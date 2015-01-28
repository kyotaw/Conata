# -*- coding: utf-8 -*-

from general import settings

from BeautifulSoup import BeautifulSoup
from BeautifulSoup import NavigableString
import os
import codecs

class YahooNewsScraper:
	def __init__(self):
		pass
	
	def scrap(self, filePath):
		if not os.path.exists(filePath):
			return u''

		with codecs.open(filePath, 'rb', 'utf_8') as html:
			h = html.read()
			h = h.encode("utf_8")
			soup = BeautifulSoup(h)
			article = soup.find('p', attrs={'class':'ynDetailText'})
			if article is None:
				return u''

			newsText = u''
			for content in article.contents:
				if isinstance(content, NavigableString):
					newsText += content
		
			return newsText
		
