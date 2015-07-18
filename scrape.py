#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re, requests, shutil

rootUrl = "http://www.bleach-mx.fr/lecture-en-ligne/"
show = "Dragon_Ball_Super"
firstEp = "Dragon_Ball_Z_1"
firstName = "Dragon Ball Z 1 - La Resurrection de [F]"

re_splitlines = re.compile(r'</[^>]+><|><')

def scrapeEpisode(episode, name, first=False):
    path = os.path.join(show, name)
    if not os.path.exists(path):
        os.makedirs(path)
    html = requests.get(rootUrl+show+"/"+episode).content
    scrapePage(episode, name, 1, html)
    status = 0
    for line in re_splitlines.split(html):
        if "Scan du Chapitre" in line or 'onchange="change_page' in line or 'title="Suivant"' in line:
            status += 1
        elif status and line.startswith("option value="):
            if first and status == 1:
                epid = line[line.find('"')+1:]
                epid = epid[:epid.find('"')]
                epname = line[line.find('>')+1:]
                scrapeEpisode(epid, epname)
            elif status == 2 and "selected" not in line:
                page = line[line.find('"')+1:]
                page = page[:page.find('"')]
                scrapePage(episode, name, page)

def scrapePage(episode, name, page, html=None):
    path = os.path.join(show, name, "%02d.jpg" % int(page))
    if os.path.exists(path):
        return
    if not html:
        html = requests.get(rootUrl+show+"/"+episode+"/"+page).content
    img = html[html.find('<img src="mangas/Dragon Ball Super/')+10:]
    img = img[:img.find('.jpg" alt="')+4]
    img = rootUrl + img
    print path
    img = requests.get(img, stream=True)
    with open(path, 'wb') as f:
        img.raw.decode_content = True
        shutil.copyfileobj(img.raw, f)

scrapeEpisode(firstEp, firstName, first=True)

