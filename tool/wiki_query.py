# -*- coding: utf-8 -*-

import urllib
import requests

def query_wikipedia(title):
    params = {
        'action':'query',
        'prop':'revisions',
        'format':'xml',
        'rvprop':'content',
        'rvparse':'',
        'titles':title,
    }
    res = requests.get('http://ja.wikipedia.org/w/api.php', params=params)
    return res.text



