# -*- coding: utf-8 -*-

from xml.sax.saxutils import unescape
from bs4 import BeautifulSoup, NavigableString, Tag

def scrap_wiki(doc):
    soup = BeautifulSoup(unicode(unescape(doc, {'&quot;':'\"'})))
    rev_tag = soup.find('rev')
    if not rev_tag:
        return u''
    
    article = u''
    for string in rev_tag.stripped_strings:
        article += string

    if article[:9] == '#REDIRECT':
        return u''

    return unicode(article)
