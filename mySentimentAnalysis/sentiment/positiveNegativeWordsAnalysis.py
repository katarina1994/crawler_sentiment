'''
Created on 2. lip 2018.

@author: Katarina123
'''

#import nltk
#nltk.download()
import codecs
from nltk.classify import NaiveBayesClassifier
import CroatianStemmer.Croatian_stemmer as stem


class PosNegExamples():


    def dictionaryOfWords(self, word):
        return dict([(word, True)])
    
    
    def getNegPos(self, testX):
        
        stemmer = stem.CroatianStemmer()       
        positiveWords = []
        negativeWords = []
        neutralWords = []
        
        f = codecs.open ("gs-sentiment-annotations.txt", 'r', encoding='Windows-1250')
        for line in f.readlines():
            line = line.split(" ")
            word = line[0]
            mark = line[1]
            mark = mark.replace('\n', '').replace('\r', '')
        
            if(mark == "+"):
                positiveWords.append(stemmer.stemOneWord(word))
            elif (mark == "-"):
                negativeWords.append(stemmer.stemOneWord(word))
            elif(mark == "0"):
                neutralWords.append(stemmer.stemOneWord(word))
            else:
                print ("Wrong input in file!")  
                
        
        positiveFeatures = [(self.dictionaryOfWords(positive), 1) for positive in positiveWords]
        negativeFeatures = [(self.dictionaryOfWords(negative), -1) for negative in negativeWords]
        neutralFeatures = [(self.dictionaryOfWords(neutral), 0) for neutral in neutralWords]
        
        trainX = negativeFeatures + positiveFeatures + neutralFeatures
        classifier = NaiveBayesClassifier.train(trainX) 
        
        
        neg = 0
        pos = 0        
        sentence = testX.lower()
        words = sentence.split(' ')
        for word in words:
            classResult = classifier.classify(self.dictionaryOfWords(word))
            if (classResult == -1):
                #print (word, classResult)
                neg += 1
            if (classResult == 1):
                #print (word, classResult)
                pos += 1
        
        if (neg != 0 or pos != 0):
            #print('Positive: ' + str(float(pos)/(pos+neg)))
            #print('Negative: ' + str(float(neg)/(pos+neg)))
            positive = float(pos)/(pos+neg)
            negative = float(neg)/(pos+neg)
            return (positive, negative)
        else:
            #print("Sentence doesn't contain any valuable words or too short!")
            return (float(0),float(0))
