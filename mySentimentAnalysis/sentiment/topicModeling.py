#!/usr/bin/env python
# -*- coding: utf-8 -*- 

'''
Created on 23. ozu 2018.

@author: Katarina123
'''


import glob
import os
from polyglot.text import Text
#import gensim
import codecs
#from gensim import corpora, models
from sklearn.feature_extraction.text import CountVectorizer
#from sklearn.datasets import fetch_20newsgroups
from sklearn.decomposition import LatentDirichletAllocation



class TopicModeling():

    # WRITE INFO ABOUT TOPIC TO FILES
    def writeTopicInfoToFile(self, listOfStemmedWords, topicNumber):    
        
            fTopic = codecs.open("topics/topic-%05d.txt" % topicNumber, 'w', encoding='Windows-1250')
            text = " ".join(listOfStemmedWords)
            fTopic.write(text)
            #print (text)
            fTopic.close()
        

    # GET ALL STOPWORDS FROM CROATIAN LANUGAGE
    def getStopWords(self):
        
        stopWords = []
        fStopWords = codecs.open("stopWords.txt", 'r', encoding='Windows-1250')
        tmp = fStopWords.readlines()
        for w in tmp:
            w = w.strip("\n")
            stopWords.append(w)
        fStopWords.close()
        return stopWords
        
        
    # TIME TO WORK WITH EACH ARTICLE, FIND KEY WORDS FROM IT AND WRITE THEM TO FILE 
    def writeKeyWordsToFile(self, path, topicNumber, numberOfPages):
        
        allKeyWordsFromArticles = []
        allKeyWordsFromArticlesStemmed = []
        documents = []
        originalStemmedDocuments = []

        allFiles = glob.glob(os.path.join(path, '*.txt'))
        topicNumber = topicNumber - numberOfPages
        #print (topicNumber)

        #index = 1
        while (topicNumber < len(allFiles)):
        #for fileName in glob.glob(os.path.join(path, '*.txt')):
            f = open(allFiles[topicNumber], "r");
            doc = ""
            docOriginal = ""
            for line in f.readlines():
                line = line.strip(" ").strip("\t").strip("\n").strip("\r").strip()
                originalStemmedDocuments.append(line)
                lineSplitted = line.split(" ")
                if(len(lineSplitted) == 1):
                    docOriginal += lineSplitted[0].strip("\n")
                    docOriginal += " "
                    doc += lineSplitted[0].strip("\n")
                    doc += " "
                else:
                    docOriginal += lineSplitted[0].strip("\n")
                    docOriginal += " "
                    doc += lineSplitted[1].strip("\n")
                    doc += " "
                
            documents = [doc]
            #print (index)
            #print (documents)
            # LDA
            stopWords = self.getStopWords()
            tf_vectorizer = CountVectorizer(max_df=2, min_df=1, max_features=100, stop_words=stopWords, analyzer='word')
            tf = tf_vectorizer.fit_transform(documents)
            tf_feature_names = tf_vectorizer.get_feature_names()
        
            # Run LDA
            lda = LatentDirichletAllocation(n_components=1, max_iter=5, learning_method='online', learning_offset=50.,random_state=0).fit(tf)
        
            noKeyWords = 20
            for _tID, topic in enumerate(lda.components_):
                listOfOriginalWords = []
                listOfStemmedWords = []
                for i in topic.argsort()[:-noKeyWords - 1:-1]:
                    #print (tf_feature_names[i])
                    for line in originalStemmedDocuments:
                        line = line.split(" ")
                        if(len(line) > 1):
                            if(tf_feature_names[i] == line[1].lower()):
                                #print (tf_feature_names[i], line[0].lower())
                                listOfOriginalWords.append(line[0])
                                listOfStemmedWords.append(line[1])
                                break    
                self.writeTopicInfoToFile(listOfStemmedWords, topicNumber)
                
            allKeyWordsFromArticles.append(listOfOriginalWords)
            textStemmedWords = Text(" ".join(listOfStemmedWords), hint_language_code='hr')
            allKeyWordsFromArticlesStemmed.append(textStemmedWords.sentences[0])    
            topicNumber += 1
            documents = []
            originalStemmedDocuments = []     
            #print (allKeyWordsFromArticles)
            #index += 1
        return allKeyWordsFromArticlesStemmed
    
    