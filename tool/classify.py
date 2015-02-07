# -*- coding: utf-8 -*-

import os
import datetime
import sys
import pickle
from Conata.env import path
from Conata.classifier.area_classifier import AreaClassifier
from nlang.processor.tokenizer import Tokenizer
from nlang.base.util.util import pp

#t = Tokenizer()
#with open('takatuku2.txt', 'r') as f:
#    w = t.tag(f.read().decode('utf_8'))

#lem = []
#for word in w:
#    lem.append(word['lemma'])
#print pp(lem)

start = datetime.datetime.now()

#ac = AreaClassifier(path.get_area_root(), recursive=int(0))
with open('area_classifier.pickle', 'rb') as f:
    ac = pickle.load(f)
with open('test.txt', 'r') as f:
    print( pp(ac.classify(f.read())))

time = datetime.datetime.now() - start

print(pp(ac._AreaClassifier__classifier.informative_features(10)))

with open('area_classifier.pickle', 'wb') as f:
    pickle.dump(ac, f)

print('completed! time : ' + str(time.seconds) + ' sec')
