#!/usr/bin/env python
# -*- coding: utf-8 -*- 

'''
Created on 19. tra 2018.

@author: Katarina123
'''



import re
import glob
import os
import codecs
import spiders.myFirstSpider as sp
#import spiders.roundRobinSpider as rrsp
import spiders.cleanTextParser as ctp
import CroatianStemmer.Croatian_stemmer as stem
import sentiment.topicModeling as tm
import sentiment.personRecommender as pr
import sentiment.cataloguePersonHelper as cph
import sentiment.modelSVM as model
#from sentiment import cataloguePersonHelper
import sentiment.positiveNegativeWordsAnalysis as posneg


# START CRAWLER AND CLEAN ARTICLE TEXT
def runCrawl():
    
    #REGULAR SPIDER
    fConfig = open("configurationFiles/config.txt", "r");
    domain = fConfig.readline().strip("\n")
    regexExpr = fConfig.readline().strip("\n")
    numberOfPages = fConfig.readline()
    fConfig.close()
    
    fAll = codecs.open("allLinks.txt", 'a+', encoding='Windows-1250')
    numberOfLinksBeforeCrawl = sum(1 for _line in open('allLinks.txt'))
    regularSpiderCrawl = sp.RegularSpider()
    
    regularSpiderCrawl.spider("https://" + domain, domain, regexExpr, int(numberOfPages), fAll, numberOfLinksBeforeCrawl)
    fAll.close()


    """
    #ROUDN ROBIN -> fix "if url not in allLines" (don't save already saved articles)
    domains = []
    regexExpressions = []
    howManyPagesToCrawl = 0
    
    f_RRconfig = open("configurationFiles/roundRobinConfig.txt", 'r');
    numberVisited = sum(1 for line in open('allLinks.txt'))
    howManyPagesToCrawl = int(f_RRconfig.readline())
    while 1:
        line = f_RRconfig.readline().strip("\n").split(",")#strip("[").strip("]").strip("\n")
        if not line[0]:
            break
        #print (line)
        domains.append(line[0])
        regexExpressions.append(line[1])
    
    pagesToVisit = []
    for domain in domains:
        pagesToVisit.append("https://" + domain)
    
    fAll = codecs.open("allLinks.txt", 'a', encoding='Windows-1250')
    roundRobinSpiderCrawl = rrsp.RoundRobinSpider()
    links = roundRobinSpiderCrawl.roundRobinSpider(pagesToVisit, domains, regexExpressions, howManyPagesToCrawl, fAll, numberVisited)
    fAll.close()
    """
    
    numberOfLinks = sum(1 for _line in open('allLinks.txt'))
    print (numberOfLinks)
    # Get clean text from articles HTML and write it to file
    cleanTextParser = ctp.CleanText()
    cleanTextParser.writeCleanTextAndTitlesFromHtmlToFile("allLinks.txt", numberOfLinks, int(numberOfPages))
    
    # Get stemmed words from clean text of atricles
    stemmer = stem.CroatianStemmer()
    stemmer.stemWords(numberOfLinksBeforeCrawl)
    




# FIND ARTICLE TOPICS, RUN NER, HELP WITH CATALOUGE-TITLES
def runAnalizeTopicSaveDB():
        
    fConfig = open("configurationFiles/config.txt", "r");
    numberOfPages = fConfig.readlines()[2]
    fConfig.close()
    numberOfLinks = sum(1 for _line in open('allLinks.txt'))
    
    
    # MAKNIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII !!!!!!!!!!!!!!1
    #numberOfLinks = 0
    #numberOfPages = 0  
    
    cleanTextParser = ctp.CleanText()
    
    # Get all links of all articles
    fPerson = open('allLinks.txt')
    personLinks = fPerson.readlines()  
    fPerson.close()
    
    # Get all persons from DB
    catalogue = cph.CatalogueHelper()
    listOfAllPersonsFromDB = catalogue.getPersonFromDB()
    
    # Find topic with LDA and write them to file
    getArticleTopic = tm.TopicModeling()
    allKeyWordsStemmed = getArticleTopic.writeKeyWordsToFile("stemmedWords/", numberOfLinks, int(numberOfPages)) 
       
    
    # Run Name Entity Recognition over all articles,
    # get help from DB (key words and titles),
    # get right person from DB (person table) 
    # and save person info to DB (personinfo table)
    matchedPersonInDB = []
    
    
    # Perform NER and get all names from all articles
    allPersonNER = []
    getNER = pr.NER()
    personsFromArticlesFoundByNER = getNER.getNERFromText("topics/", numberOfLinks, int(numberOfPages))
    for articlePerson in personsFromArticlesFoundByNER:
        allPersonNER += cleanTextParser.getPolyglotSentenceList(articlePerson)
    matchedPersonInDB += catalogue.compareTextWithPersonFromDB(allPersonNER, listOfAllPersonsFromDB, personLinks, numberOfLinks, int(numberOfPages))
    print (matchedPersonInDB)
    
    
    # Go through key words from article text and save right person info to DB
    matchedPersonInDB += catalogue.compareTextWithPersonFromDB(allKeyWordsStemmed, listOfAllPersonsFromDB, personLinks, numberOfLinks, int(numberOfPages))
    print (matchedPersonInDB)
    
    
    # Go through title text and sve right person info to DB
    # 400 JER SAD TESTIRAM PO SVIMA POPRAVI ZA DOBIT SAMO ZADNJE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    allTitles = cleanTextParser.getAllTitlesOfArticles(numberOfLinks, int(numberOfPages))
    matchedPersonInDB += catalogue.compareTextWithPersonFromDB(allTitles, listOfAllPersonsFromDB, personLinks, numberOfLinks, int(numberOfPages))
    print (matchedPersonInDB)
   
    # Now we have all the right persons to save to DB :)
    listOfFiles = os.listdir("matchedArticle/")
    numberFiles = len(listOfFiles)

    matchedPersonInDB = list(set(matchedPersonInDB)) 
    numberMatched = numberFiles
    for person in matchedPersonInDB:
        print (person)
        print (numberMatched)
        link = person[1]
        articleText = cleanTextParser.getOneArticleText(link)
        f = codecs.open("matchedArticle/article-%05d.txt" % numberMatched, 'w', encoding='Windows-1250')
        f.write(articleText.encode('Windows-1250', 'replace').decode('Windows-1250', 'replace'))
        f.close()
        numberMatched += 1
        
    
    # SAVING TO DB !!
    #matchedPersonInDB = list(set(matchedPersonInDB)) # to get rid of duplicates in list       
    for personDB in matchedPersonInDB:
        catalogue.savePersonInfoToDB(personDB)
    




# NO MACHINE LEARNING -> FIND EVERY PERSON MENTIONED IN ARTICLE (NOT TOPIC-PERSON)
# YOU CAN PROBABLY USE compareTextWithPersonFromDB -> as text just use whole article..., check this...
def runFindPersonAppearanceInArticle():
    
    stemmer = stem.CroatianStemmer()
    
    fConfig = open("configurationFiles/config.txt", "r");
    numberOfPages = fConfig.readlines()[2]
    fConfig.close()
    numberOfLinks = sum(1 for _line in open('allLinks.txt'))
    
    fPerson = open('allLinks.txt')
    personLinks = fPerson.readlines()  
    fPerson.close()
    
    cleanTextParser = ctp.CleanText()
    listOfAllArticles = cleanTextParser.getAllArticlesText("allLinks.txt", numberOfLinks, int(numberOfPages))
    catalogue = cph.CatalogueHelper()
    listOfAllPersonsFromDB = catalogue.getPersonFromDB()
    
    allArtilces = []
    for article in listOfAllArticles:
        article = article.split(" ")
        article = [stemmer.stemOneWord(word) for word in article]
        article = [word for word in article if word is not None]
        article = cleanTextParser.getPolyglotSentenceList(article)
        allArtilces += article

    matchedPersonInDB = []
    matchedPersonInDB += catalogue.compareTextWithPersonFromDB(allArtilces, listOfAllPersonsFromDB, personLinks, numberOfLinks, int(numberOfPages))
            
    for person in matchedPersonInDB:
        print (person)
           
    return matchedPersonInDB     
           
    
    
# SENTIMENT ANALYSIS BY USING PREVIOUSLY EVALUETED POSITIVE AND NEGATIVE WORDS (1, -1)           
def rungetsentimentAnalysisFromPosAndNegWords():
       
    pn = posneg.PosNegExamples()
    stemmer = stem.CroatianStemmer()
    topicM = tm.TopicModeling()   
    stopwords = topicM.getStopWords()


    # GET ALL ARTICLES RELEVANT FOR CROATIAN PUBLIC PERSONS
    articles = []
    path = "matchedArticle"
    for fileName in glob.glob(os.path.join(path, '*.txt')):
            f = open(fileName, "r");
            articles += f.readlines()
            f.close  
  
  
  
    # FOREACH ARTICLE
    for article in articles:
        
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
        article = [[ word if (word not in stopwords) else '' for word in sentence] for sentence in article]             
        
        
        # STEM ARTICLE TEXT      
        article = [" ".join(sentence) for sentence in article] 
        article = [stemmer.stemArticle(sentence) for sentence in article]
        #print (article)
        
        
        # GET ANALYSIS BY USING "POSITIVE" AND "NEGATIVE" WORDS
        posAnalysisArticleText = 0
        negAnalysisArticleText = 0
        numOfSent = 0
        for sentence in article:
            #print (" ".join(sentence))
            sent = " ".join(sentence)
            pos = pn.getNegPos(sent)[0]
            neg = pn.getNegPos(sent)[1]
            posAnalysisArticleText += pos
            negAnalysisArticleText += neg
            if (neg != 0 or pos != 0):
                numOfSent += 1
        if (numOfSent != 0):
            posArticle = float(posAnalysisArticleText/numOfSent)
            negArticle = float(negAnalysisArticleText/numOfSent)
            neuArticle = float(1 - posArticle - negArticle)
        else:
            posArticle = 0.0
            negArticle = 0.0
            neuArticle = 1.0
        print (article)
        print (posArticle, negArticle, neuArticle)
        
        
        
# SENTIMENT ANALYSIS BY USING SVM MODEL (TEST AND TRAIN)          
def rungetsentimentAnalysisSVMModel():
    
    path = "matchedArticle"
    svm = model.SVM()
    result = svm.trainAndTestSVMModel(path)
    return result
    
    