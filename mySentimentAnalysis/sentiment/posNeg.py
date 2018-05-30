#!/usr/bin/env python
# -*- coding: utf-8 -*- 

'''
Created on 20. svi 2018.

@author: Katarina123
'''


import codecs
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


articles = []
path = "matchedArticle"
for fileName in glob.glob(os.path.join(path, '*.txt')):
        f = open(fileName, "r");
        articles += f.readlines()
        f.close

for article in articles:
    print (article)
    stemmedArticle = stemmer.stemArticle(article)
    print (stemmedArticle)
    print ("\n")

"""
# WE NEED TO TRAIN OUR MODEL
features = vectorizer.fit_transform(data)
features_nd = features.toarray()
X_train, X_test, y_train, y_test  = train_test_split(
        features_nd, 
        data_labels,
        train_size=0.80, 
        random_state=None)

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