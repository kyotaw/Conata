# -*- coding: utf-8 -*-

import csv
import sys
import os
from Conata.env import path

if len(sys.argv) < 2:
    print('usage make_japan_address_folders.py address_file')
    quit()

csv_file = sys.argv[1]

with open(csv_file, 'rb') as f:
    csv_reader = csv.reader(f)
    for row in csv_reader:
        dirs = '/'.join([path.get_area_root()] + [area for area in row[7:] if area != ''])
        if not os.path.exists(dirs):
            print('make dir : ' + dirs)
            os.makedirs(dirs.decode('utf_8'))
