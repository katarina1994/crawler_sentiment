'''
Created on 15. ozu 2018.

@author: Katarina123
'''

#import nltk
#nltk.download()

from polyglot.text import Text
import os
import nltk
import glob

path = "C:/Users/Katarina123/workspace/mySpider/spiders/cleanTextFromHTML/"

for fileName in glob.glob(os.path.join(path, '*.txt')):
    file = open(fileName, "r");
    readL = file.readlines()
    textFromPage = ""
    for rl in readL:
        textFromPage += rl.strip()
    cleanedTextFromPage = ""
    sent_text = nltk.sent_tokenize(textFromPage)
    for sent in sent_text:
        if "." in sent:
            sent = sent.split(".")
            for s in sent:
                cleanedTextFromPage += s
                cleanedTextFromPage += " "
        else:
            cleanedTextFromPage += sent
            cleanedTextFromPage += " "

    #print (cleanedTextFromPage)
    text = Text(cleanedTextFromPage, hint_language_code='hr')
    person = []
    for sent in text.sentences:
        #print(sent, "\n")
        for entity in sent.entities:
            #print (entity)
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
