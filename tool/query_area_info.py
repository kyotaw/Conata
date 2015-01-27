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
ignore_folders = [scraped_text_folder, '１丁目', '２丁目', '３丁目']

log_file = codecs.open('wiki_query.log', 'w')

def extract_characteristic_area_name(delim, area_name):
    query = ''
    if delim in area_name:
        tokens = area_name.split(delim)
        if len(tokens) >= 2:
            query = delim.join(tokens[1:])
        else:
            query = tokens[0] + delim 
    return query

def get_query_word(area_name):
    query = extract_characteristic_area_name('郡', area_name)
    if query != '':
        return query
    query = extract_characteristic_area_name('町', area_name)
    if query != '':
        return query
    query = extract_characteristic_area_name('大字', area_name)
    if query != '':
        return query
    return area_name

for dir_path, sub_dirs, file_names in os.walk(area_root):
    dir_name = os.path.basename(dir_path)
    if dir_name in ignore_folders:
        log_file.write('skip ' + dir_name + '\n') 
        continue
   
    folder_path = '/'.join([dir_path, scraped_text_folder])
    file_path = '/'.join([folder_path, 'wiki_' + dir_name + '.txt'])
    if not overwrite and os.path.exists(file_path):
        print(dir_name + ' already queried')
        continue
  
    query = get_query_word(dir_name)
   
    log = dir_name + ' talk to wikipedia using keyword : ' + query
    print(log)
    log_file.write(log + '\n')

    xml = query_wikipedia(dir_name)
    if xml != '':
        text = scrap_wiki(xml)
    else:
        log_file.write('wiki page for ' + dir_name + ' not found\n') 

    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    with open(file_path, 'wb') as f:
        f.write(text.encode('utf_8'))

    time.sleep(1)

err_file.close()
