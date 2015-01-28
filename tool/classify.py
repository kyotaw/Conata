# -*- coding: utf-8 -*-

import os
from Conata.env import path
from Conata.area_classifier.area_classifier import AreaClassifier
from nlang.processor.tokenizer import Tokenizer
from nlang.base.util.util import pp

#t = Tokenizer()
#with open('takatuku2.txt', 'r') as f:
#    w = t.tag(f.read().decode('utf_8'))

#lem = []
#for word in w:
#    lem.append(word['lemma'])
#print pp(lem)

ac = AreaClassifier(path.get_area_root(), recursive=False)
with open('test.txt', 'r') as f:
    print pp(ac.classify(f.read().decode('utf_8')))
