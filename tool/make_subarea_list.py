# -*- coding: utf-8 -*-

import csv
import sys
import os
from Conata.env import path
from nlang.base.data.trie import Trie

if len(sys.argv) < 2:
    print('usage make_japan_address_folders.py address_file')
    quit()

csv_file = sys.argv[1]
area_tree = {} 
with open(csv_file, 'rb') as f:
    csv_reader = csv.reader(f)
    for row in csv_reader:
        address = [area for area in row[7:] if area != '']
        parent = '/'.join(address[:-1]) if len(address) > 1 else '' 
        sub_area = address[-1] if len(address) > 1 else address[0]
        if parent not in area_tree:
            area_tree[parent] = []
        if sub_area != '':
            area_tree[parent].append(sub_area)

for parent, subarea_list in area_tree.items():
    list_path = '/'.join([path.get_area_root(), parent, 'subarea_list'])
    print('writing subarea_list to ' + list_path)
    with open(list_path, 'w') as f:
        for area in subarea_list:
            if area != '':
                print('subarea : ' + area)
                f.write(area + '\n')


