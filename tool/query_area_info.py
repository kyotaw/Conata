# -*- coding: utf-8 -*-

import os
import time
import sys
import codecs
import datetime
from nlang.processor.tokenizer import Tokenizer
from nlang.base.util.util import pp
from Conata.tool.wiki_query import query_wikipedia
from Conata.tool.wiki_scraper import scrap_wiki
from Conata.env import path

if len(sys.argv) < 2:
    print('usage query_area_info.py overwrite search_area_file')
    quit()

overwrite = False
if len(sys.argv) > 1:
    overwrite = True if int(sys.argv[1]) > 0 else False

def read_lines(list, file):
    line = file.readline()
    while line:
        list.append(line[:-1])
        line = file.readline()

area_root = path.get_area_root()
scraped_text_folder = 'topics'
ignore_folders = [scraped_text_folder, '１丁目', '２丁目', '３丁目', '４丁目', '５丁目', '６丁目']

log_file = codecs.open('wiki_query.log', 'w')

address_delim_list = []
with open(path.get_address_root() + '/address_delimiter') as f:
    read_lines(address_delim_list, f)

def get_dir_filter():
    search_area_list = []
    search_area_file = ''
    if len(sys.argv) > 2:
        search_area_file = sys.argv[2]
        with open(search_area_file, 'r') as f:
            read_lines(search_area_list, f)

    def filter_dir(dir_name):
        return True if search_area_file == '' or dir_name in search_area_list else False
    return filter_dir

def get_area_filter():
    address_filter_list = []
    with open(path.get_address_root() + '/address_filter') as f:
        read_lines(address_filter_list, f) 
    
    def filter_area(area_name):
        return True if area_name in address_filter_list else False
    return filter_area

filter_dir = get_dir_filter()
filter_area = get_area_filter()

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
    if filter_area(area_name):
        return area_name
    
    for delim in address_delim_list:
        query = extract_characteristic_area_name(delim, area_name)
        if query != '':
            return query
    
    return area_name

start = datetime.datetime.now()

for dir_path, sub_dirs, file_names in os.walk(area_root):
    dir_name = os.path.basename(dir_path)
    if dir_name in ignore_folders:
        log_file.write('skip ' + dir_path + '\n') 
        continue

    if not filter_dir(dir_name):
        continue
   
    folder_path = '/'.join([dir_path, scraped_text_folder])
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    
    file_path = '/'.join([folder_path, 'wiki_' + dir_name + '.txt'])
    if not overwrite and os.path.exists(file_path):
        print(dir_path + ' already queried')
        continue
  
    query = get_query_word(dir_name)
   
    log = dir_path + ' talk to wikipedia using keyword : ' + query
    print(log)
    log_file.write(log + '\n')

    xml = query_wikipedia(query)
    text = scrap_wiki(xml)
    if text == u'':
        log = 'wiki page for ' + dir_name + ' not found'
        print(log)
        log_file.write(log + '\n')
    with open(file_path, 'wb') as f:
        f.write(text.encode('utf_8'))

    time.sleep(2)

log_file.close()

time = datetime.datetime.now() - start
print('completed! time : ' + str(time.seconds) + ' sec')
