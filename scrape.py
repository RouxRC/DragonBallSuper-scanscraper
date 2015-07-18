#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, re
import requests
import shutil

rootUrl = "http://www.bleach-mx.fr/lecture-en-ligne/"

re_splitlines = re.compile(r'</[^>]+><|><')

def scrapeEpisode(title, episode='', name='', first=False):
    html = requests.get(rootUrl+title+"/"+episode).content
    if name:
        path = os.path.join('scans', title, name)
        if not os.path.exists(path):
            os.makedirs(path)
        scrapePage(title, episode, name, 1, html=html)
    status = 0
    for line in re_splitlines.split(html):
        if "Scan du Chapitre" in line or 'onchange="change_page' in line or 'title="Suivant"' in line:
            status += 1
        elif status and line.startswith("option value="):
            if first and status == 1:
                epid = line[line.find('"')+1:]
                epid = epid[:epid.find('"')]
                epname = line[line.find('>')+1:]
                scrapeEpisode(title, episode=epid, name=epname)
            elif name and status == 2 and "selected" not in line:
                page = line[line.find('"')+1:]
                page = page[:page.find('"')]
                scrapePage(title, episode, name, page)

def scrapePage(title, episode, name, page, html=None):
    path = os.path.join("scans", title, name, "%02d.jpg" % int(page))
    if os.path.exists(path):
        return
    if not html:
        html = requests.get(rootUrl+title+"/"+episode+"/"+page).content
    img = html[html.find('<img src="mangas/')+10:]
    img = img[:img.find('.jpg" alt="')+4]
    img = rootUrl + img
    print path
    img = requests.get(img, stream=True)
    with open(path, 'wb') as f:
        img.raw.decode_content = True
        shutil.copyfileobj(img.raw, f)

if __name__ == "__main__":
    scrapeEpisode(sys.argv[1], first=True)
