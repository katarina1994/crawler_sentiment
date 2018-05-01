#!/usr/bin/env python
# -*- coding: utf-8 -*- 

'''
Created on 19. tra 2018.

@author: Katarina123
'''


import codecs
import spiders.myFirstSpider as sp
#import spiders.roundRobinSpider as rrsp
import spiders.cleanTextParser as ctp
import CroatianStemmer.Croatian_stemmer as stem
import sentiment.topicModeling as tm
import sentiment.personRecommender as pr
#import sentiment.personRecommender as recomm



def runCrawlAndSentiment():
    
    
    #REGULAR SPIDER
    fConfig = open("configurationFiles/config.txt", "r");
    domain = fConfig.readline().strip("\n")
    regexExpr = fConfig.readline().strip("\n")
    numberOfPages = fConfig.readline()

    fAll = codecs.open("allLinks.txt", 'a+', encoding='Windows-1250')
    numberOfLinks = sum(1 for line in open('allLinks.txt'))
    regularSpiderCrawl = sp.RegularSpider()
    
    regularSpiderCrawl.spider("https://" + domain, domain, regexExpr, int(numberOfPages), fAll, numberOfLinks)
    fAll.close()


    """
    #ROUDN ROBIN
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
    
    
    # Get cleane text from articles
    cleanTextParser = ctp.CleanText()
    cleanTextParser.getCleanTextFromHtml(numberOfLinks)
    
    # Get stemmed words from clean text of atricles
    stemmer = stem.CroatianStemmer()
    stemmer.stemWords(numberOfLinks)
    
    # Find topic with LDA
    getArticleTopic = tm.TopicModeling()
    getArticleTopic.getKeyWords("stemmedWords/", numberOfLinks)
    getArticleTopic.getTitleInfo("allTitles.txt", numberOfLinks)
    
    # Name Entity Recognition
    getNER = pr.NER()
    getNER.getNERFromText("topics/", numberOfLinks)
    
    """  
    listOfAllpersonsBD = getNER.getPersonFromDB()
    listStemmedPersonDB = []
    for person in listOfAllpersonsBD:
        partSurname = person[2]
        partSurname = partSurname.split(" ")
        for part in partSurname:
            #print (stemmer.stemOneWord(part))
            listStemmedPersonDB.append(stemmer.stemOneWord(part))

    
    fTitles = codecs.open("allTitles.txt", 'r')
    allTitles = fTitles.readlines()  
    allTitles = [title.lower().strip().strip(" ").strip("\n").strip("\t").strip("\r") for title in allTitles]
    allTitles = [oneTitle.split(" ") for oneTitle in allTitles]
    allTitles = [[word.strip(".").strip(",").strip("'").strip(":").strip(";").strip("-").strip("!").strip("?").strip("+") for word in oneTitle] for oneTitle in allTitles]
    allTitles = [[stemmer.stemOneWord(word) for word in oneTitle] for oneTitle in allTitles]
    fTitles.close()

    helpToNER = []
    numbOfTopic = 1
    for title in allTitles:
        #print (title)
        for word in title:
            #print (word)
            for personDB in listStemmedPersonDB:
                #print (personDB.lower(), word)
                if (word == personDB.lower()):
                    helpToNER.append((word, numbOfTopic))
        numbOfTopic += 1   
        
    print (helpToNER)
    """
#runCrawlAndSentiment()

