# -*- coding: utf-8 -*-

from yahoo_news_scraper import YahooNewsScraper
from general import settings

import sys
import os

if __name__ == '__main__':
	if len(sys.argv) < 2:
		quit()

	inRootDir = sys.argv[1]
	outRootDir = inRootDir.replace(settings.RAW_HTML_EXPORT_PATH, settings.SCRAPED_TEXT_EXPORT_PATH)
	if not os.path.exists(outRootDir):
		os.makedirs(outRootDir)

	for dirPath, subDirs, fileNames in os.walk(inRootDir):
		exportDir = dirPath.replace(settings.RAW_HTML_EXPORT_PATH, settings.SCRAPED_TEXT_EXPORT_PATH) + '/'
		if not os.path.exists(exportDir):
			os.mkdir(exportDir)
		
		for fileName in fileNames:
			filePath = os.path.join(dirPath, fileName)
			yahoo = YahooNewsScraper()
			text = yahoo.scrap(filePath)
			exportFilePath = exportDir + fileName
			with open(exportFilePath, 'wb') as f:
				f.write(text.encode('utf_8'))

