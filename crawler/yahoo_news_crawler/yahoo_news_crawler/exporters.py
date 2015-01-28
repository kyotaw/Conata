# -*- coding: utf-8 -*-

from scrapy.contrib.exporter import BaseItemExporter

from Conata.general.util import util

import os
import re
import codecs
from urlparse import urlparse

class RawHtmlExporter(BaseItemExporter):
	def __init__(self, dir):
		self.exportDir = dir
		if not os.path.exists(self.exportDir):
			os.makedirs(self.exportDir)

	def export_item(self, item):
		url = urlparse(item["url"])
		path = re.sub(r"[\/:*?\"<>|]", ".", url.path + url.query + url.params).lstrip(".")
                utf8 = util.to_utf8(item['body'], item['encoding'])
		if utf8 is None:
			return item

		with codecs.open(self.exportDir + path, "wb", 'utf_8') as f:
			f.write(utf8.decode('utf_8'))
		return item
		
