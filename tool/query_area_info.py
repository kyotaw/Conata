# -*- coding: utf-8 -*-

import os
import time
import sys
import codecs
from nlang.processor.tokenizer import Tokenizer
from nlang.base.util.util import pp
from Conata.tool.wiki_query import query_wikipedia
from Conata.tool.wiki_scraper import scrap_wiki
from Conata.env import path

overwrite = False
if len(sys.argv) > 1:
    overwrite = True if int(sys.argv[1]) > 0 else False

area_root = path.get_area_root()
scraped_text_folder = 'topics'
ignore_folders = [scraped_text_folder]

err_file = codecs.open('query_error', 'w')

for dir_path, sub_dirs, file_names in os.walk(area_root):
    dir_name = os.path.basename(dir_path)
    if dir_name in ignore_folders:
        continue
    
    folder_path = '/'.join([dir_path, scraped_text_folder])
    file_path = '/'.join([folder_path, 'wiki_' + dir_name + '.txt'])
    if not overwrite and os.path.exists(file_path):
        print(dir_name + ' already queried')
        continue
   
    query = ''
    tokens = dir_name.split('郡')
    if len(tokens) > 2:
        err_file.write("invalid city name :" + dir_name + '\n')
    elif len(tokens) == 2:
       query = tokens[1]
    else:
        query = dir_name

    print('query info for : ' + query)
    xml = query_wikipedia(dir_name)
    text = scrap_wiki(xml)

    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    with open(file_path, 'wb') as f:
        f.write(text.encode('utf_8'))

    time.sleep(1)

err_file.close()
