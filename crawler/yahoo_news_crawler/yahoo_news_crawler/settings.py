# -*- coding: utf-8 -*-

# Scrapy settings for crime_crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'yahoo_news_crawler'

SPIDER_MODULES = ['yahoo_news_crawler.spiders']
NEWSPIDER_MODULE = 'yahoo_news_crawler.spiders'

DOWNLOAD_DELAY = 3
ROBOTSTXT = True
COOKIES_ENABLED = False

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'yahoo_news_crawler (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
	'yahoo_news_crawler.pipelines.RawHtmlExportPipeline' : 100,
}
