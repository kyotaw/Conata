# -*- coding: utf-8 -*-

import os

CONATA_ROOT = os.path.dirname(os.path.abspath(__file__))[:-4]

def get_area_root():
    return '/'.join([CONATA_ROOT, 'data', 'world', '日本'])
