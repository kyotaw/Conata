# -*- coding: utf-8 -*-

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from yahoo_news_crawler.items import RawHtmlItem

class RawHtmlSpider(CrawlSpider):
	name = 'yahoo_news'
	allowed_domains = [
		'news.yahoo.co.jp',
		'headlines.yahoo.co.jp'
	]
	start_urls = [
#		'http://news.yahoo.co.jp/list/?c=domestic',
#		'http://news.yahoo.co.jp/list/?c=world',
#		'http://news.yahoo.co.jp/list/?c=economy',
#		'http://news.yahoo.co.jp/list/?c=entertainment',
#		'http://news.yahoo.co.jp/list/?c=sports',
#		'http://news.yahoo.co.jp/list/?c=computer',
#		'http://news.yahoo.co.jp/list/?c=science',
		'http://news.yahoo.co.jp/list/?c=local',
	]
	
	rules = [
		Rule(LxmlLinkExtractor(restrict_xpaths="//a[@class='next']", unique=True)),
		Rule(LxmlLinkExtractor(allow=(r'pickup'), unique=True)),
		Rule(LxmlLinkExtractor(restrict_xpaths="//div[@class='headlineTxt']/a[@class='newsLink']"), callback="parse_article"),
	]

	def parse_article(self, response):
		htmlRes = HtmlResponse(url=response.url, body=response.body)
		item = RawHtmlItem();
		item["url"] = htmlRes.url
		item["body"] = htmlRes.body
		item["encoding"] = htmlRes.encoding
		return item


