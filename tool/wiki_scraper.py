# -*- coding: utf-8 -*-

from xml.sax.saxutils import unescape
from bs4 import BeautifulSoup, NavigableString, Tag

def scrap_wiki(doc):
	soup = BeautifulSoup(unicode(unescape(doc, {'&quot;':'\"'})))
	
	warning = soup.find('warnings')
        if warning:
            warning.decompose()

        navi = soup.find('table', class_='navbox')
        if navi:
            navi.decompose()
	
	article = u''
	for string in soup.stripped_strings:
		article += string

	if article[:9] == '#REDIRECT':
		return u''

	return unicode(article)
