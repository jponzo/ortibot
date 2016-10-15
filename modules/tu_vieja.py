#!/usr/bin/python
# -*- coding: utf-8 -*-


import yaml
import os
import random
class TuVieja(object):

    def __init__(self, mood="messages"):
        self.mood = mood

    def puteada(self, subject):
        imHere = os.path.dirname(os.path.abspath(__file__))
        with open("%s/../%s.yaml" % (imHere,self.mood), 'r') as ymlfile:
            config = yaml.load(ymlfile)
        if subject in config:
            return random.choice(config[subject])
        else:
            return random.choice(config['default'])

    def setMood(self, NewMood):
        self.mood = NewMood
        return self.mood
