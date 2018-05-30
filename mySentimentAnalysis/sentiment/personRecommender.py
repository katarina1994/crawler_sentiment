'''
Created on 15. ozu 2018.

@author: Katarina123
'''

#import nltk
#nltk.download()

from polyglot.text import Text
import os
#import nltk
import glob


class NER():
    
    
    # FIND PERSON FROM ARTICLES WITH NER
    def getNERFromText(self, path, topicNumber, numberOfPages):

        allFiles = glob.glob(os.path.join(path, '*.txt'))
        allTopicPersonsFoundByNER = [] 
        topicNumber = topicNumber - numberOfPages
        
        while (topicNumber < len(allFiles)):
            file = open(allFiles[topicNumber], "r");
            textOfTopic = file.readlines()[0]                 
            text = Text(textOfTopic, hint_language_code='hr')
            person = []
            if(text):
                #print (text.sentences)
                #allKeyWords[:] += list(text.sentences)
                for entity in text.entities:
                        #print (entity)
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
            #print (person)           
            allTopicPersonsFoundByNER.append(person)
            topicNumber += 1
        return allTopicPersonsFoundByNER
       