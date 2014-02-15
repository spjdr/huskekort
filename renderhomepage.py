#!/usr/bin/env python
#coding=utf-8

import json
import os
from subprocess import call 
import shutil
import time

purge = True
update = {'previews': True, 'pdf': True, 'manifest': True, 'index': True, 'credits': True}

def touchdir(direc):
    if (not os.path.isdir(direc)):
        os.makedirs(direc)


# iterate through cards 
f = open('resources/data/cards.json','r')
cards = json.loads(f.read())
f.close()


f = open('resources/data/images.json','r')
images = json.loads(f.read())
f.close()

# purge all 
if (purge and os.path.isdir('homepage/kort')):
    shutil.rmtree('homepage/kort')


# update preview PNGs (and make card folders)
if (update['previews']):
    # cmd = '/Applications/Inkscape.app/Contents/Resources/bin/inkscape "huskekort.pdf" -z --export-dpi=72 --export-area-drawing --export-png="huskekort.png"'
    cmd = 'convert -density 300 tex/huskekort.pdf -resize 33% huskekort.png'
    call(cmd,shell=True) 

    i = 0
    for card in cards:
        cardfolder = 'homepage/kort/' + card['name']
        if (not os.path.isdir(cardfolder)):
            os.makedirs(cardfolder)
        os.rename('huskekort-' + str(i) + '.png', cardfolder + '/' + card['name'] + '.png')
        i += 1

# update the downloadable pdfs
if (update['pdf']):

    for card in cards:
        f = 'kort/' + card['name'] + '/' + card['name'] + '.pdf'
        shutil.copyfile('tex/' + f,'homepage/' + f)

        f = 'kort/' + card['name'] + '/' + card['name'] + '_A7.pdf'
        shutil.copyfile('tex/' + f,'homepage/' + f)

        f = 'kort/' + card['name'] + '/' + card['name'] + '_A8.pdf'
        shutil.copyfile('tex/' + f,'homepage/' + f)

    touchdir('homepage/kort/alle')
    touchdir('homepage/kort/alleA7')
    touchdir('homepage/kort/alleA8')

    # copy main file
    shutil.copyfile('tex/alle.pdf','homepage/kort/alle/alle.pdf')
    shutil.copyfile('tex/alleA7.pdf','homepage/kort/alleA7/alleA7.pdf')
    shutil.copyfile('tex/alleA8.pdf','homepage/kort/alleA8/alleA8.pdf')

    # copy images from assets folder
    shutil.copyfile('homepage/assets/img/alle.png', 'homepage/kort/alle/alle.png')
    shutil.copyfile('homepage/assets/img/alleA7.png', 'homepage/kort/alleA7/alleA7.png')
    shutil.copyfile('homepage/assets/img/alleA8.png', 'homepage/kort/alleA8/alleA8.png')


# update cache manifest
if (update['manifest']):
    revision = 1
    manifest = "CACHE MANIFEST\n#rev " + str(revision) + "\nindex.php\nassets/css/screen.css\nassets/img/huskekort-icon.png\n"
    manifest += "credit.php\nassets/img/gplaypattern.png\nassets/img/single.gif\nassets/img/eightfold.gif\n"
    manifest += "assets/img/sixteenfold.gif\nkort/alle/alle.png\nkort/alleA7/alleA7.png\nkort/alleA8/alleA8.png\n"
    manifest += "http://spjdrpedia.dk/w/skins/uniform/type/Bitter-Regular-webfont.ttf\n"
    manifest += "http://spjdrpedia.dk/w/skins/uniform/type/IstokWeb-Regular-webfont.ttf\n"

    for card in cards:
        manifest += 'kort/' + card['name'] + '/' + card['name'] + '.png' + "\n"

    f = open('homepage/huskekort.manifest', 'w')
    f.write(manifest.encode('utf-8'))
    f.close()

if (update['index']):
    touchdir('homepage/kort')
    shutil.copyfile('resources/data/cards.json', 'homepage/kort/cards.json')
    shutil.copyfile('resources/data/meta.json', 'homepage/kort/meta.json')

if (update['credits']):

    ca = '<ul>'
    im = '<ul>'

    f = open('resources/data/credits.json','r')
    credits = json.loads(f.read())
    f.close()

    for i, card in enumerate(cards):
        ca += '<li>Huskekort <a href="http://spjdrpedia.dk/wiki/' + card['uri'] + '">' + card['titel'].strip() + '</a>: '
        ca += (', ').join(map(lambda s: '<a href="http://spjdrpedia.dk/wiki/Bruger:' + s.replace(' ','_') + '">' + s + '</a>', credits['cards'][i]))
        ca += '</li>'
 
        if (len(card['images'])>0):
            for image in card['images']:
                im += '<li><a href="http://spjdrpedia.dk/wiki/' + images[image].strip().replace(' ','_') + '">' + images[image].strip() + '</a>: '
                im += (', ').join(map(lambda s: '<a href="http://spjdrpedia.dk/wiki/Bruger:' + s + '">' + s + '</a>', credits['images'][image]))
            im += '</li>'
       
    html = ca + '</ul><br/>' + im + '</ul>'

    f = open('homepage/kort/credits.html','w')
    f.write(html.encode('utf-8'))
    f.close()

