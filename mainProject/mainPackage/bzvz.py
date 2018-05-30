#!/usr/bin/env python
# -*- coding: utf-8 -*- 


'''
Created on 13. svi 2018.

@author: Katarina123
'''



import codecs
import re
import CroatianStemmer.Croatian_stemmer as stem
import glob
import os
import sentiment.topicModeling as tm    
#from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cross_validation import train_test_split
#from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score



stemmer = stem.CroatianStemmer()
topicModel = tm.TopicModeling()
stopWords = topicModel.getStopWords()

vectorizer = TfidfVectorizer(
    min_df = 0.5,
    max_df = 0.8,
    sublinear_tf=True,
    use_idf=True,
    encoding = 'utf-8',
    analyzer = 'word',
    lowercase = True,
    stop_words = stopWords,    
)


data = []
data_labels = []


with open("positiveArticles.txt") as f:
    for i in f: 
        data.append(i) 
        data_labels.append('pos')
 
with open("negativeArticles.txt") as f:
    for i in f: 
        data.append(i)
        data_labels.append('neg')

"""
articles = []
path = "matchedArticle"
for fileName in glob.glob(os.path.join(path, '*.txt')):
        f = open(fileName, "r");
        articles += f.readlines()
        f.close
"""

dataInOrder = []
text = ""
for article in data:
    #print (article)
    
    # REMOVE PERSONS' STATEMENTS FROM ARTICLE
    #article = re.sub(r'\:\s\-.*?\-\s',"", article)
    article = re.sub(r'\-\s.*?\-\s',"", article)
    article = re.sub(r'\‘.*?\’',"", article)
    article = re.sub(r'\‘.*?\'',"", article)
    article = re.sub(r'\'.*?\’',"", article)
    article = re.sub(r'\'.*?\'',"", article)
    article = re.sub(r'\“.*?\”',"", article)
    article = re.sub(r'\„.*?\”',"", article)
    article = re.sub(r'\".*?\”',"", article)
    article = re.sub(r'\“.*?\"',"", article)
    article = re.sub(r'\„.*?\"',"", article)
    article = re.sub(r'\".*?\"',"", article)

    # GET SENTENCES FROM ARTICLE      
    article = article.split(".")

    # CLEAN ARTICLE TEXT FROM STOPWORDS         
    article = [sentence.split(" ") for sentence in article]  
    article = [[ word.strip(".").strip(",").strip("'").strip(":").strip(";").strip("-").strip("!").strip("?").strip("+").strip("").strip("(").strip(")").strip("/") for word in sentence] for sentence in article] 
    article = [[ word if (word not in stopWords) else '' for word in sentence] for sentence in article]             
    
    
    # STEM ARTICLE TEXT      
    article = [" ".join(sentence) for sentence in article] 
    #article = [stemmer.stemArticle(sentence) for sentence in article]
    
    #stemmedArticle = stemmer.stemArticle(article)
    #article = [" ".join(sentence) for sentence in article]
    for sentence in article:
        text += sentence
        text += ". "
    text += "\n"
    dataInOrder.append(text)
    text = ""


# WE NEED TO TRAIN OUR MODEL
features = vectorizer.fit_transform(dataInOrder)
features_nd = features.toarray()
X_train, X_test, y_train, y_test  = train_test_split(
        features_nd, 
        data_labels,
        train_size=0.70, 
        random_state=72817)

print (X_train)
print(y_train)
print (X_test)
print(y_test)

#log_model = MultinomialNB()
log_model = SVC(kernel='linear')
log_model = log_model.fit(X=X_train, y=y_train)

# TIME TO PREDICT :)
y_pred = log_model.predict(X_test)

print (X_train)
print(y_train)
print (X_test)
print(y_test)


print (y_pred)
print(accuracy_score(y_test, y_pred))















"""
import codecs
import CroatianStemmer.Croatian_stemmer as stem
import re
import glob
import os



import spiders.cleanTextParser as ctp

import codecs
from urllib.request import urlopen  

fHtml = codecs.open("allLinks.txt", 'r', encoding='Windows-1250')

links = fHtml.readlines()

c = ctp.CleanText()
html = urlopen(links[0]).read()
title = c.getDateFromHtml(html)
fHtml.close()
        



"""