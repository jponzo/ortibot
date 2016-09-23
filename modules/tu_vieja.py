#!/usr/bin/python
# -*- coding: utf-8 -*-


import yaml
import os
import random
class TuVieja(object):

    def puteada(self, subject):
        imHere = os.path.dirname(os.path.abspath(__file__))
        with open("%s/../messages.yaml" % imHere, 'r') as ymlfile:
            config = yaml.load(ymlfile)
        if subject in config:
            return config[subject]
            
        else:
            return random.choice(config['default'])