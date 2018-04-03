#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#import nltk
# Corpus which consists of male and female names dataset
#from nltk.corpus import names
# For shuffling
#import random
#from sklearn.naive_bayes import GaussianNB
#import numpy as np

#import polyglot
from polyglot.text import Text, Word
#from polyglot.downloader import downloader

"""

#print(downloader.supported_languages_table("ner2", 3))


blob = """"""
text = Text(blob, hint_language_code='hr')
person = []
for sent in text.sentences:
    print(sent, "\n")
    for entity in sent.entities:
        if(entity.tag == "I-PER"):
            #print (entity)
            if (len(entity) > 1):
                name = ""
                for en in entity:
                    #print (en)
                    name = name + en + " "
                name = name.strip(" ")
                if(name not in person):
                    person.append(name)
                    
print (person)
"""

words = ["Ivane", "imate", "li", "možda", "ispovjedaonicu"]
for w in words:
    w = Word(w, language="hr")
    print(w, "  ", w.morphemes)
