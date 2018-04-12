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


class NER():
    
    def getNEROfTopics(self):
        path = "C:/Users/Katarina123/workspace/mySentimentAnalysis/sentiment/topics/"

        for fileName in glob.glob(os.path.join(path, '*.txt')):
            file = open(fileName, "r");
            textOfTopic = file.readlines()[0]
            #print (readL)
            
            
            text = Text(textOfTopic, hint_language_code='hr')
            person = []
            if(text):
                print (text.sentences)
                for entity in text.entities:
                        print (entity)
                        if(entity.tag == "I-PER"):
                            #print (entity)
                            if (len(entity) >= 1):
                                name = ""
                                for en in entity:
                                    #print (en)
                                    name = name + en + " "
                                
                                name = name.strip(" ")
                                if(name not in person):
                                    person.append(name)              
            print (person)
