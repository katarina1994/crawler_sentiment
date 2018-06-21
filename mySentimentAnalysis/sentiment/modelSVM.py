'''
Created on 7. lip 2018.

@author: Katarina123
'''

import re
#import CroatianStemmer.Croatian_stemmer as stem
import glob
import os
import sentiment.topicModeling as tm    
#from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cross_validation import train_test_split
#from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
#from sklearn.svm import SVC
from sklearn.metrics import accuracy_score



class SVM():


    def transformInputData(self, data, stopWords):
    
        dataInOrder = []
        text = ""
        for article in data:
            #print (article)
            article = article.strip("\n")
            article = article.replace(u'\xa0', u'')
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
        return dataInOrder
    
    
    
    
    def trainAndTestSVMModel(self, path):
        
        
        topicModel = tm.TopicModeling()
        stopWords = topicModel.getStopWordsNoNegative()
        vectorizer = TfidfVectorizer(
            min_df = 0.1,
            max_df = 0.8,
            sublinear_tf=True,
            use_idf=True,
            encoding = 'utf-8',
            analyzer = 'word',
            lowercase = True,
            stop_words = stopWords,    
        )
        
        
        data = []
        dataLabelsTrain = []
        
        
        with open("positiveArticles.txt") as f:
            for i in f: 
                data.append(i) 
                dataLabelsTrain.append('pos')
        
        with open("negativeArticles.txt") as f:
            for i in f: 
                data.append(i)
                dataLabelsTrain.append('neg')
        
        with open("neutralArticles.txt") as f:
            for i in f: 
                data.append(i)
                dataLabelsTrain.append('neu')
        
        
        
        articles = []
        for fileName in glob.glob(os.path.join(path, '*.txt')):
                with open(fileName) as f:
                    for i in f: 
                        articles.append(i)
        
        
        dataTrain = self.transformInputData(data, stopWords)
        dataTest = self.transformInputData(articles, stopWords)
        
        # WE NEED TO TRAIN OUR MODEL
        featuresTrain = vectorizer.fit_transform(dataTrain)
        featuresNDTrain = featuresTrain.toarray()
        
        X_train, X_test, y_train, y_test  = train_test_split(
                featuresNDTrain, 
                dataLabelsTrain,
                train_size=0.80, 
                random_state=72817)
        
        
        print (X_train)
        print(y_train)
        print (X_test)
        print(y_test)
        
        
        
        """
        #log_model = MultinomialNB()
        log_model = SVC(kernel='linear')
        log_model = log_model.fit(X=X_train, y=y_train)
        
        # TIME TO PREDICT :)
        y_pred = log_model.predict(X_test)
        
        print (y_pred)
        print(accuracy_score(y_test, y_pred))
        """
        
        
        log_model = LinearSVC()
        log_model.fit(X_train, y_train)
        y_pred = log_model.predict(X_test)
        score = log_model.score(X_test, y_test)
        print (score)
        print(accuracy_score(y_test, y_pred))
        
        featuresTest = vectorizer.transform(dataTest)
        featuresNDTest = featuresTest.toarray()
        y_predArticles = log_model.predict(featuresNDTest)
        #print (dataTest)
        print (y_predArticles)
        return y_predArticles
