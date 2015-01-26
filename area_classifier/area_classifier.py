# -*- coding: utf-8 -*-

import os
from nlang.classifier.naive_bayes_classifier import NaiveBayesClassifier
from nlang.processor.tokenizer import Tokenizer
from nlang.base.util.util import pp

class AreaClassifier(object):
    def __init__(self, area_path, parent_classifiers={}, recursive=True, tokenizer=None):
        self.__classifier = None 
        self.__subarea_classifiers = {}
        self.__parent_classifiers = parent_classifiers
        self.__area_path = area_path
        subarea_file_path = '/'.join([area_path, 'subarea_list'])
        if not os.path.exists(subarea_file_path):
            print(subarea_file_path + ' not exists')
            return
        
        self.__classifier = NaiveBayesClassifier()
        self.__tokenizer = tokenizer
        if not self.__tokenizer:
            self.__tokenizer = Tokenizer()
        with open(subarea_file_path, 'r') as f:
            subarea = f.readline()[:-1]
            while subarea:
                subarea_path = '/'.join([self.__area_path, subarea])
                self.__train_subarea(subarea, subarea_path)
                if recursive:
                    pc = self.__parent_classifiers.copy()
                    pc[subarea] = self.__classifier
                    self.__subarea_classifiers[subarea.decode('utf_8')] = AreaClassifier(
                        subarea_path, pc, recursive=True, tokenizer=self.__tokenizer)
                subarea = f.readline()[:-1]
    
    def classify(self, text):
        if not self.__classifier:
            return []
        tagged_words = self.__tokenizer.tag(text)
        words = [w['lemma'] for w in tagged_words]
        areas = []
        area = self.__classifier.classify({'word':words})
        areas.append(area)
        if area in self.__subarea_classifiers:
            areas += self.__subarea_classifiers[area].classify(text)
        return areas

    def train(self, subarea, text):
        tagged_words = self.__tokenizer.tag(text)
        words = [w['lemma'] for w in tagged_words]
        train_data = (subarea.decode('utf_8'), {'word':words})
        self.__classifier.train((subarea.decode('utf_8'), {'word':words}))
        for area, classifier in self.__parent_classifiers.items():
            print('also parent area: ' + area)
            classifier.train((area.decode('utf_8'), {'word':words}))
    
    def __train_subarea(self, subarea, subarea_path):
        if not os.path.exists(subarea_path):
            print(subarea_path + ' not exists')
            return
        topics_path = '/'.join([subarea_path, 'topics'])
        if not os.path.exists(topics_path):
            print(topics_path + ' not exists')
            return
        
        for dir_path, sub_dirs, file_names in os.walk(topics_path):
            for file in file_names:
                file_path = '/'.join([topics_path, file])
                with open(file_path, 'r') as f:
                    self.train(subarea, f.read().decode('utf_8'))

