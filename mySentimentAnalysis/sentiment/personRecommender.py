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
        
        
        


#POKUSAJI KLASIFIKATORA - MANJE VISE USPJESNO...
"""
def custom_tokenize(text):
    if not text:
        print('The text to be tokenized is a None type. Defaulting to blank string.')
        text = ''
    return nltk.word_tokenize(text)

def extract_entities(text):
    for sent in nltk.sent_tokenize(text):
        print (sent)
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label'):
                print (chunk.label(), ' '.join(c[0] for c in chunk.leaves()))


def get_human_names(text):
    tokens = nltk.tokenize.word_tokenize(text)
    pos = nltk.pos_tag(tokens)
    sentt = nltk.ne_chunk(pos, binary = False)
    person_list = []
    person = []
    name = ""
    for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
        for leaf in subtree.leaves():
            person.append(leaf[0])
        if len(person) > 1:
            for part in person:
                name += part + ' '
            if name[:-1] not in person_list:
                person_list.append(name[:-1])
            name = ''
        person = []

    return (person_list)

#extract_entities(text)
names = get_human_names(text)
print (names)
"""
        