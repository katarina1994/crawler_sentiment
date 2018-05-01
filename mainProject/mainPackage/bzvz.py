'''
Created on 30. tra 2018.

@author: Katarina123
'''
import codecs
import glob
import os

fAll = codecs.open("allLinks.txt", 'r', encoding='Windows-1250')
url = "https://www.jutarnji.hr/domidizajn/interijeri/rustikalna-kuca-koju-su-sagradili-ribari/7285720/"
if not any(line == url for line in fAll):
    print (url)