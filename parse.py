#!/usr/bin/env python
#coding=utf-8

# install via 'pip install requests'
import requests 
import json
import re
from io import open as iopen
from urlparse import urlsplit
import urllib
import replacer
from subprocess import call
import time

# update = {'data': False, 'images': False, 'icons': False, 'credits': False}
update = {'data': True, 'images': False, 'icons': False, 'credits': False}


def requests_image(file_dest,file_url):
    suffix_list = ['jpg', 'gif', 'png', 'tif', 'svg',]
    file_name =  urlsplit(file_url)[2].split('/')[-1]
    file_suffix = file_name.split('.')[1]
    i = requests.get(file_url)
    if file_suffix in suffix_list and i.status_code == requests.codes.ok:
        with iopen(file_dest, 'wb') as file:
            file.write(i.content)
    else:
        return False

def get_images(images,folder):

    if (len(images)>20):
        get_images(images[0:19],folder)
        get_images(images[20:],folder)
    else:
        r = requests.get('http://spjdrpedia.dk/w/api.php?format=json&action=query&titles=%s&prop=imageinfo&iiprop=url' % "|".join(images))
        response = r.json()
        # print images
        for member in response['query']['pages']:
            print member
            if int(member)>0:
                url = response['query']['pages'][member]['imageinfo'][0]['url']

                name = response['query']['pages'][member]['title'].encode('utf-8').split(':')[1]
                name = name.replace(' ','_').replace('(','\(').replace(')','\)')

                requests_image(folder + name ,url)

                if name.split('.')[1]=='svg':            
                    cmd = '/Applications/Inkscape.app/Contents/Resources/bin/inkscape ' + folder + name + ' --export-pdf=' + folder + name.split('.')[0] + '.pdf'
                    call(cmd,shell=True) # convert


# update
if (update['data']):

    # get list of huskekort 
    r = requests.get('http://spjdrpedia.dk/w/api.php?format=json&action=query&list=categorymembers&cmtitle=Kategori:Huskekort&cmlimit=100')
    response = r.json()

    # init
    titles = []

    for member in response['query']['categorymembers']:
        titles.append(member['title'])


    r = requests.get("http://spjdrpedia.dk/w/api.php?format=json&action=query&titles=%s&prop=revisions&rvprop=content" % '|'.join(titles))
    response = r.json()

    f = open('resources/data/response.txt', 'w')
    f.write(json.dumps(response).encode('utf8'))
    f.close()

    meta = {'updated': time.strftime('%d/%m/%Y')}
    f = open('resources/data/meta.json', 'w')
    f.write(json.dumps(meta).encode('utf8'))
    f.close()

    # for pages in response['query']['pages']:
else:

    f = open('resources/data/response.txt','r')
    response = json.loads(f.read());
    # json.load(response)
    f.close()

# remove some info
cs = []
for page in response['query']['pages']:
    if response['query']['pages'][page]['title'] == 'Huskekort/Skabeloner':
        continue
    cs.append({'text': response['query']['pages'][page]['revisions'][0]['*'], 'title': response['query']['pages'][page]['title']})
    
# regexp to match
p = re.compile('^(\w+)=(.+)$',re.DOTALL)

# replacements
replacements = (u'æ', u'ae'), (u'ø', u'oe'), (u'å', u'aa')

cards = []
images = []
for c in cs:
    card = {'uri': c['title'],'emne': ''}
    for ci in c['text'].split('|'):
        m = p.match(ci)
        if m:
            # print m.group(1)
            card[m.group(1)] = m.group(2)
    name = replacer.multiple_replace(card['titel'].strip().lower(),*replacements)
    card['name'] = urllib.quote_plus(name.encode('utf-8'))
    if (len(card)>0):
        card['images'] = []
        if 'billede' in card:
            images.append(card['billede'])
            card['images'].append(len(images)-1)
        if 'billede2' in card:
            images.append(card['billede2'])
            card['images'].append(len(images)-1)
        cards.append(card)


# sort cards
cards = sorted(cards, key = lambda card: card['titel'])  # secondary sort by titel
cards = sorted(cards, key = lambda card: card['emne'])   # primary sort by emne

# save cards
f = open('resources/data/cards.json', 'w')
f.write(json.dumps(cards).encode('utf8'))
f.close()

# save images
f = open('resources/data/images.json', 'w')
f.write(json.dumps(images).encode('utf8'))
f.close()

# get images
if update['images']:
    get_images(images,'./resources/images/')

# update icons
if update['icons']:
    r = requests.get('http://spjdrpedia.dk/w/api.php?format=json&action=query&titles=Ambidexter&prop=images&imlimit=100')
    response = r.json()

    icons = []
    for imgs in response['query']['pages']['570']['images']:
        icons.append(imgs['title'])

    get_images(icons,'./resources/icons/')

# update credits
if update['credits']:
    credits = {'cards': [], 'images': list([])}

    for i, image in enumerate(images):
        r = requests.get("http://spjdrpedia.dk/w/api.php?format=json&action=query&titles=%s&prop=revisions&rvprop=user&rvlimit=100" % image.strip())
        response = r.json()
        content = response['query']['pages'][(response['query']['pages'].keys())[0]]
        credits['images'].append(list(set([ w['user'] for w in content['revisions']])))

    for card in cards:
        r = requests.get("http://spjdrpedia.dk/w/api.php?format=json&action=query&titles=%s&prop=revisions&rvprop=user&rvlimit=100" % card['uri'].strip())
        response = r.json()
        content = response['query']['pages'][(response['query']['pages'].keys())[0]]
        credits['cards'].append( list(set([ w['user'] for w in content['revisions']])) )

    f = open('resources/data/credits.json', 'w')
    f.write(json.dumps(credits).encode('utf8'))
    f.close()
else:
    f = open('resources/data/credits.json','r')
    credits = json.loads(f.read());
    # json.load(response)
    f.close()





