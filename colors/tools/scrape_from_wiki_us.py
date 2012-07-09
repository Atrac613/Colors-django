# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
import urllib2
import simplejson

url = 'http://en.wikipedia.org/wiki/List_of_colors'

req = urllib2.Request(url, headers={'User-Agent': "Magic Browser"})
srcHtml = urllib2.urlopen(req).read()

soup = BeautifulSoup(srcHtml, fromEncoding="utf-8")

color_names = []

for row in soup.findAll('tr'):
    if len(row) == 25:
        td = row.findAll('td')
        hex_str = None
        if len(td) == 11:
            hex_str = td[1].contents[0].string.strip()

        th = row.findAll('th')
        name_str = None
        if len(th) == 1:
            name_str = str(th[0].contents[0].string)

        if hex_str and name_str:
            color_names.append({'name': name_str, 'hex': hex_str})

print simplejson.dumps(color_names)
