# -*- coding: utf-8 -*-

import os
from Conata.config import options


CONATA_ROOT = os.path.dirname(os.path.abspath(__file__))[:-4]

def get_area_root():
    option = __get_option('AREA_ROOT')
    return option if option != '' else '/'.join([CONATA_ROOT, 'data', 'world', '日本'])

def get_raw_html_export_path():
    option = __get_option('RAW_HTML_EXPORT_PATH')
    return option if option != '' else '/'.join([CONATA_ROOT, 'data', 'raw_html'])

def __get_option(item):
	return options[item] if item in options else ''
