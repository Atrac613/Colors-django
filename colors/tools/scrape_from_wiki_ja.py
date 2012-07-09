# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
import urllib2
import simplejson

def get_color_list_page(soup):
    urls = []
    urls.append(url)

    for row in soup.findAll('tr'):
        if len(row) in (23, 17):
            td = row.findAll('td')
            if len(td) in (11, 8):
                for a in td:
                    a = a.find('a')
                    if a is not None:
                        urls.append('%s%s' %  (domain, a['href']))
    return urls

def get_color_names(urls):
    color_names = []
    for url in urls:
        req = urllib2.Request(url, headers={'User-Agent': "Magic Browser"})
        srcHtml = urllib2.urlopen(req).read()

        soup = BeautifulSoup(srcHtml, fromEncoding="utf-8")

        try:
            for row in soup.findAll('tr'):
                if len(row) == 11:
                    td = row.findAll('td')
                    hex_str = None
                    if len(td) == 3:
                        hex_str = td[0].contents[1].string.strip()

                    th = row.findAll('th')
                    yomi_str = None
                    kanji_str = None
                    if len(th) == 2:
                        yomi_str = str(th[0].contents[0].string)
                        kanji_str = str(th[1].contents[0].string)

                    if hex_str and yomi_str and kanji_str:
                        color_name = {'hex': hex_str, 'yomi': yomi_str, 'kanji': kanji_str}
                        color_names.append(color_name)
        except:
            pass

    return color_names

domain = 'http://ja.wikipedia.org'
url = domain + '/wiki/%E8%89%B2%E5%90%8D%E4%B8%80%E8%A6%A7_(%E3%81%82)'

req = urllib2.Request(url, headers={'User-Agent': "Magic Browser"})
srcHtml = urllib2.urlopen(req).read()

soup = BeautifulSoup(srcHtml, fromEncoding="utf-8")

urls = get_color_list_page(soup)
color_names = get_color_names(urls)

print simplejson.dumps(color_names)
