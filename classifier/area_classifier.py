# -*- coding: utf-8 -*-

import os
import re
import threading
from nlang.classifier.naive_bayes_classifier import NaiveBayesClassifier
from nlang.processor.tokenizer import Tokenizer
from nlang.processor.chunker import Chunker
from nlang.base.util.util import pp

class AreaClassifier(object):
    @staticmethod
    def __init_subarea(self, subarea):
        subarea_path = '/'.join([self.__area_path, subarea])
        pc = self.__parent_classifiers.copy()
        pc[subarea] = self.__classifier
        self.__subarea_classifiers[subarea] = AreaClassifier(subarea_path, pc, self.__recursive)


    def __init__(self, area_path, parent_classifiers={}, recursive=True, inclusive=False):
        self.__classifier = None 
        self.__subarea_classifiers = {}
        self.__parent_classifiers = parent_classifiers
        self.__area_path = area_path
        self.__recursive = recursive
        self.__inclusive = inclusive
        subarea_file_path = '/'.join([area_path, 'subarea_list'])
        if not os.path.exists(subarea_file_path):
            print(area_path + ' has no sub area')
            return
        
        self.__classifier = NaiveBayesClassifier()
        self.__tokenizer = Tokenizer()
        self.__chunker = Chunker()

        subarea_list = []
        with open(subarea_file_path, 'r') as f:
            subarea = f.readline()[:-1]
            while subarea:
                subarea_list.append(subarea)
                subarea = f.readline()[:-1]
        
        subarea_thread_list = []
        max_thread_count = 12
        thread_count = max_thread_count
        if self.__is_recursive():
            for subarea in subarea_list:
                if thread_count > 0:
                    thread = threading.Thread(target=AreaClassifier.__init_subarea, name=subarea, args=(self, subarea))
                    thread.start()
                    subarea_thread_list.append(thread)
                    thread_count -= 1
                else:
                    AreaClassifier.__init_subarea(self, subarea)
                    for thread in subarea_thread_list:
                        thread.join()
                    thread_count = max_thread_count
                    subarea_thread_list = []

        for subarea in subarea_list:
            self.__train_subarea(subarea)
        
        for thread in subarea_thread_list:
            thread.join()
                 
        #print(pp(self.__classifier.informative_features(5)))
    
    def classify(self, text):
        if not self.__classifier:
            return []
        areas = []
        self.__classify(areas, self.__get_feature(text))
        return areas

    def train(self, subarea, text):
        features = self.__get_feature(text)
        self.__classifier.train((subarea, features))
        
        if self.__inclusive:
            for area, classifier in self.__parent_classifiers.items():
                print(area + ' also learning about ' + subarea)
                classifier.train((area, features))
    
   
    def __classify(self, areas, features):
        area = self.__classifier.classify(features)
        areas.append(area)
        if area in self.__subarea_classifiers:
            self.__subarea_classifiers[area]._AreaClassifier__classify(areas, features)
        
    def __train_subarea(self, subarea):
        subarea_path = '/'.join([self.__area_path, subarea])
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
                print(self.__area_path + ' learning about ' + subarea + ' with ' + file_path)
                with open(file_path, 'r') as f:
                    self.train(subarea, f.read())
    
    def __get_feature(self, text):
        tagged_words = self.__tokenizer.tag(text)
        pattern = re.compile('^N-PROPN')
        #pattern = re.compile('^N-.[^U]')
        nouns = [w['lemma'] for w in tagged_words if pattern.search(w['pos'])]
        #clause = self.__chunker.clause(nouns)
        #words = [''.join(c) for c in clause]
        return {'word':nouns}

    def __is_recursive(self):
        if isinstance(self.__recursive, bool):
            return self.__recursive
        elif isinstance(self.__recursive, int):
            if self.__recursive > 0:
                self.__recursive -= 1
                return True
            else:
                return False
        else:
            return False

