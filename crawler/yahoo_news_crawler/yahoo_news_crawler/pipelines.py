# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import datetime
import os
from urlparse import urlparse
from scrapy import signals
from Conata.crawler.yahoo_news_crawler.yahoo_news_crawler.exporters import RawHtmlExporter
from Conata.env import path

class RawHtmlExportPipeline(object):
	@classmethod
	def from_crawler(cls, crawler):
		pipeline = cls()
		crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
		crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
		return pipeline

	def __init__(self):
		self.exportRoot = ""
		self.exporters = {}

	def spider_opened(self, spider):
		date = datetime.date.today()
		self.exportRoot = path.get_raw_html_export_path() + '/' + spider.name + "/" + str(date.year) + "." + str(date.month) + "." + str(date.day) + "/"

	def spider_closed(self, spider):
		for exporter in self.exporters[domain]:
			exporter.finish_exporting()
	
	def process_item(self, item, spider):
		domain = urlparse(item["url"]).netloc
		if domain not in self.exporters:
			exporter = RawHtmlExporter(self.exportRoot + domain + "/")
			exporter.start_exporting()
			self.exporters[domain] = exporter
		self.exporters[domain].export_item(item)
		return item
