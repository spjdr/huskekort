#!/usr/bin/env python
#coding=utf-8

# install via 'pip install requests'
import json
import re
from subprocess import call
from PyPDF2 import PdfFileWriter, PdfFileReader
import os


update = {'tex': True, 'credits': False}

# categories matched to icons
categories = {
    'orientering': 'compass_tilted',
    'inspiration': 'light_bulb',
    'iagttagelse': 'eye',
    'madlavning': 'food',
    'pionering': 'trileg',
    'knob': 'trefoil_knot',
    'koder': 'puzzle_lock',
    'knob': 'trefoil_knot',
    'signalering': 'signal_flags'
}

# format as latex
def latexcard(card):
    
    title = card['titel'].strip()

    text = ''
    if 'billede' in card:
        width = '1'
        if 'billed_bredde' in card:
            m = re.match(r'^\d+',card['billed_bredde'])
            if m:
                width = str(float(m.group())/420)
        billede = card['billede'].split(':')[1]
        billede = billede.replace(' ','_').split('.')[0]
        text = '\n\n{\\centering \\includegraphics[width=' + width + '\\textwidth]{../resources/images/' + billede.strip() + '}\n\n}'

    category = '';
    if 'emne' in card:
        emne = card['emne'].strip()
        if emne in categories:
            category = '\\includegraphics[width=7mm]{../resources/icons/Ad_' + categories[card['emne'].strip()] + '}'

    if 'tekst' in card:
        text += html2tex(card['tekst'])

    if 'billede2' in card:
        if len(card['billede2'].split(':')) > 1:
            width = '1'
            if 'billed2_bredde' in card:
                m = re.match(r'^\d+',card['billed2_bredde'])
                if m:
                    width = str(float(m.group())/420)
            billede = card['billede2'].split(':')[1]
            billede = billede.replace(' ','_').split('.')[0]
            text += '\n\n{\\centering \\includegraphics[width=' + width + '\\textwidth]{../resources/images/' + billede + '}\n\n}'

    if 'roteret' in card:
        tex = '\\rcard{' + title + '}{' + category +'}{' + text + '}'
    else:
        tex = '\\card{' + title + '}{' + category +'}{' + text + '}'

    return tex

# extremely simple parser
def html2tex(text):
    
    p = re.finditer(r'<(/{0,1})(\w+)(.*?)(/{0,1})>',' '+text)

    opens = {
        'b': '\\textbf{',
        'i': '\\textit{',
        'p': '',
        'br': '\n\n\\vspace{-1.3mm}',
        'ol': '\\begin{enumerate}',
        'ul': '\\begin{itemize}',
        'li': '\\item{',
        'center': '\n\n{\\centering',
        'u': '\\underline{',
        'table': '\\taburowcolors [1] 2{gray!30 .. white}\\begin{tabu} to \\textwidth ',
        'tr': '',
        'th': '\\textbf{',
        'td': ''
    }

    closes = {
        'b': '}',
        'i': '}',
        'p': '\n\n',
        'ol': '\\end{enumerate}',
        'ul': '\\end{itemize}',
        'li': '}',
        'center': '\n\n}',
        'u': '}',
        'table' : '\\end{tabu}',
        'tr' : '\\\\ \\tabucline -',
        'th' : ' } & ',
        'td' : ' & '
    }

    tags = []
    prev = 0
    for m in p:
        tags.append({'tag': 'plain', 'type': 'close', 'start': prev, 'end': m.start()-1})
        if (m.group(1)=='/'):
            # chunks.append(closes[m.group(2)])
            tags.append({'tag': m.group(2), 'type': 'close', 'start': m.start(), 'end': m.end()})
        else:
            # chunks.append(opens[m.group(2)])
            tags.append({'tag': m.group(2), 'type': 'open', 'start': m.start(), 'end': m.end()})
        prev = m.end()-1

    if (prev< len(text)):
        tags.append({'tag': 'plain', 'type': 'close', 'start': prev, 'end': len(text)-1})

    chunks = []
    for (t,m) in enumerate(tags):

        if (tags[t]['tag'] == 'plain'):
            chunks.append(text[tags[t]['start']:tags[t]['end']])
            continue

        if (tags[t]['tag'] == 'td' and tags[t+2]['tag'] == 'tr'):
            continue

        if (tags[t]['tag'] == 'th' and tags[t+2]['tag'] == 'tr'):
            chunks.append('}')
            continue

        # if (tags[t]['tag'] == 'tr' and tags[t+2]['tag']=='table'):
        #     continue

        if ( tags[t]['tag'] == 'table' and tags[t]['type'] == 'open'):
            nrows = 0
            i = t+1
            while (tags[i]['tag'] != 'tr' or tags[i]['type'] != 'close'):
                if ((tags[i]['tag'] == 'td' or tags[i]['tag'] == 'th') and tags[i]['type'] == 'open'):
                    nrows += 1
                i += 1
                if (nrows > 10 or i > 100):
                    break
            chunks.append(opens['table'] + '{' + '|X[l,1] '*nrows +'|} \\tabucline -')
            continue

        if (tags[t]['type']=='open'):
            chunks.append(opens[tags[t]['tag']])
        elif (tags[t]['type']=='close'):
            chunks.append(closes[tags[t]['tag']])

    return (''.join(chunks)).strip()


# Get cards source
f = open('resources/data/cards.json','r')
cards = json.loads(f.read());
f.close()

# get list of images
f = open('resources/data/images.json','r')
images = json.loads(f.read());
f.close()

# build huskekort.pdf of all cards
if (update['tex'] or not os.path.exists('tex/huskekort.pdf')):
    # build latex
    latex = ''
    for card in cards:
        latex += latexcard(card) + '\\newpage'

    # save latex
    f = open('tex/all.tex','w')
    f.write(latex.encode('utf-8'))
    f.close()

    # compile it (twice to make tikz behave)
    cmd = 'cd tex; xelatex huskekort.tex'
    call(cmd, shell=True)
    call(cmd, shell=True)

# build all credits
if (update['credits']):

    # load the credits
    f = open('resources/data/credits.json','r')
    credits = json.loads(f.read())
    f.close()

    # make credits
    fullcacredits = ''
    fullimcredits = ''
    for i, card in enumerate(cards):
        
        cacredit = 'Huskekort \href{http://spjdrpedia.dk/wiki/' + card['uri'] + '}{' + card['titel'].strip() + '}: '
        cacredit += (', ').join(map(lambda s: '\href{http://spjdrpedia.dk/wiki/Bruger:' + s.replace(' ','_') + '}{' + s.replace('_','\\_') + '}', credits['cards'][i]))

        imcredit = ''
        if (len(card['images'])>0):
            for image in card['images']:
                imcredit += '\href{http://spjdrpedia.dk/wiki/' + images[image].strip().replace(' ','_') + '}{' + images[image].strip().replace('_','\\_') + '}: '
                imcredit += (', ').join(map(lambda s: '\href{http://spjdrpedia.dk/wiki/Bruger:' + s.replace(' ','_') + '}{' + s.replace('_','\\_') + '}', credits['images'][image]))

        credit = cacredit + '\\newline ' + imcredit

        cardfolder = 'tex/kort/' + card['name']
        if (not os.path.isdir(cardfolder)):
            os.makedirs(cardfolder)

        f = open(cardfolder + '/credits.tex','w')
        f.write(credit.encode('utf-8'))
        f.close()

        fullcacredits += cacredit + '\\newline '
        if (imcredit != ''):
            fullimcredits += imcredit + '\\newline '

    fullcredits = fullcacredits + '\\newline ' +  fullimcredits

    f = open('tex/fullcredits.tex','w')
    f.write(fullcredits.encode('utf-8'))
    f.close()

    cmd = 'pdflatex --output-directory=tex "\def\card{tex/fullcredits} \input{tex/credits.tex}"'
    call(cmd, shell=True)

    for card in cards:
        cardfolder = 'tex/kort/' + card['name']
        if (os.path.exists(cardfolder + '/credits.tex')):
            cmd = 'pdflatex --output-directory=' + cardfolder + ' "\def\card{' + cardfolder + '/credits} \input{tex/credits.tex}"'
            call(cmd, shell=True)


# combineA7
cmd = 'cd tex; pdflatex combineA7.tex'
call(cmd, shell=True)

# alleA7.pdf
cardpdf =  PdfFileReader(open('tex/combineA7.pdf','rb'))
bagpdf = PdfFileReader('tex/bagsideA7.pdf', "rb")
creditpdf = PdfFileReader('tex/credits.pdf', "rb")
output = PdfFileWriter()
for i in xrange(cardpdf.numPages):
    output.addPage(cardpdf.getPage(i))
    output.addPage(bagpdf.getPage(0))
for i in xrange(creditpdf.numPages):
    output.addPage(creditpdf.getPage(i))
with open('tex/alleA7.pdf','wb') as outputStream:
    output.write(outputStream)

# combineA8
cmd = 'cd tex; pdflatex combineA8.tex'
call(cmd, shell=True)

# alleA8.pdf
cardpdf =  PdfFileReader(open('tex/combineA8.pdf','rb'))
bagpdf = PdfFileReader('tex/bagsideA8.pdf', "rb")
output = PdfFileWriter()
for i in xrange(cardpdf.numPages):
    output.addPage(cardpdf.getPage(i))
    output.addPage(bagpdf.getPage(0))
for i in xrange(creditpdf.numPages):
    output.addPage(creditpdf.getPage(i))
with open('tex/alleA8.pdf','wb') as outputStream:
    output.write(outputStream)

# build the single page output and the individual pdf files also
inputpdf = PdfFileReader(open("tex/huskekort.pdf", "rb"))
fulloutput = PdfFileWriter()
bagpdf = PdfFileReader(open("tex/bagside.pdf", "rb"))

j = 0 # other iterator
for i in xrange(inputpdf.numPages):
    output = PdfFileWriter()
    output.addPage(inputpdf.getPage(i))
    fulloutput.addPage(inputpdf.getPage(i))
    fulloutput.addPage(bagpdf.getPage(0))
    # does the folder exist?
    if (not os.path.isdir("tex/kort/" + cards[j]['name'])):
            os.makedirs("tex/kort/" + cards[j]['name'])
    with open("tex/kort/" + cards[j]['name'] + "/" + cards[j]['name'] + "_card.pdf", "wb") as outputStream:
        output.write(outputStream)
    j += 1

for i in xrange(creditpdf.numPages):
    fulloutput.addPage(creditpdf.getPage(i))
with open('tex/alle.pdf','wb') as outputStream:
    fulloutput.write(outputStream)

# build all the card pdfs
for card in cards:
    cardfolder = 'tex/kort/' + card['name']
    # build full version
    cardpdf = PdfFileReader(open(cardfolder+'/' + card['name'] + '_card.pdf', "rb"))
    bagpdf = PdfFileReader('tex/bagside.pdf', "rb")
    creditpdf = PdfFileReader(open(cardfolder+'/credits.pdf', "rb"))
    output = PdfFileWriter()
    # cardpdf sizing
    cardpdf = cardpdf.getPage(0)
    cardpdf.scale(2.829,2.829)
    output.addPage(cardpdf)
    # add bagside
    bagpdf = bagpdf.getPage(0)
    bagpdf.scale(2.829,2.829)
    output.addPage(bagpdf)
    # add credits
    for i in xrange(creditpdf.numPages):
        output.addPage(creditpdf.getPage(i))
    with open(cardfolder + '/' + card['name'] + '.pdf', 'wb') as outputStream:
        output.write(outputStream)

    # build A7 version
    cardfile = cardfolder + '/' + card['name']
    cardcredits = cardfolder  + '/credits'

    cmd = 'pdflatex --output-directory=' + cardfolder + ' "\def\card{' + cardfile + '_card} \def\credits{' + cardcredits + '} \input{tex/cloneA7}"'
    call(cmd, shell=True)

    cardpdf = PdfFileReader(open(cardfolder + '/cloneA7.pdf', 'rb'))
    bagpdf = PdfFileReader('tex/bagsideA7.pdf', "rb")
    output = PdfFileWriter()
    output.addPage(cardpdf.getPage(0))
    output.addPage(bagpdf.getPage(0))
    for i in xrange(creditpdf.numPages):
        output.addPage(creditpdf.getPage(i))
    with open(cardfile + '_A7.pdf', 'wb') as outputStream:
        output.write(outputStream)

    # build A8 version
    cmd = 'pdflatex --output-directory=' + cardfolder + ' "\def\card{' + cardfile + '_card} \def\credits{' + cardcredits + '} \input{tex/cloneA8}"'
    call(cmd, shell=True)

    cardpdf = PdfFileReader(open(cardfolder + '/cloneA8.pdf', 'rb'))
    bagpdf = PdfFileReader('tex/bagsideA8.pdf', "rb")
    output = PdfFileWriter()
    output.addPage(cardpdf.getPage(0))
    output.addPage(bagpdf.getPage(0))
    for i in xrange(creditpdf.numPages):
        output.addPage(creditpdf.getPage(i))
    with open(cardfile + '_A8.pdf', 'wb') as outputStream:
        output.write(outputStream)
