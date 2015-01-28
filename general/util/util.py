# -*- coding: utf-8 -*-

def to_utf8(string, guess=''):
    encodings = [
        'shift_jis', 'cp932', 'euc_jp', 'utf_8',
	'euc_jis_2004', 'euc_jisx0213', 'iso2022_jp', 'iso2022_jp_1',
	'iso2022_jp_2', 'iso2022_jp_2004', 'iso2022_jp_3', 'iso2022_jp_ext',
	'shift_jis_2004', 'shift_jisx0213', 'utf_16','utf_16_be',
	'utf_16_le', 'utf_7', 'utf_8_sig'
    ]
    if guess != '':
        encodings.insert(0, guess)
    for encoding in encodings:
	try:
	    u = string.decode(encoding)
	    return u.encode('utf_8')
	except: pass
    return None

