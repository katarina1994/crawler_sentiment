#!/usr/bin/env python
# -*- coding: utf-8 -*- 
'''
Created on 6. svi 2018.

@author: Katarina123
'''



import MySQLdb
import CroatianStemmer.Croatian_stemmer as stem
import spiders.cleanTextParser as ctp
from polyglot.text import Text


class CatalogueHelper():
        


    # COMPARE WORDS WITH PERSONS FROM DB
    def compareTextWithPersonFromDB (self, allWords, listOfAllPersonsFromDB, personLinks, topicNumber, numberOfPages):
        
        stemmer = stem.CroatianStemmer()
        allPersonFromDBInfo = []

    
        allWords = [sentence.split(" ") for sentence in allWords]
        allWords = [[word.lower() for word in sentence] for sentence in allWords]   
        allWords = [Text(" ".join(sentence), hint_language_code='hr').sentences[0] for sentence in allWords]
        
        for personDB in listOfAllPersonsFromDB:
            idP = personDB[0]
            name = personDB[1]
            surname = personDB[2]
            tag = personDB[3]
            allPersonFromDBInfo.append((idP, name, surname, tag))
        
        listOfFoundPerson = dict()


        index = topicNumber - numberOfPages
        for sentence in allWords:
            sentence = sentence.split(" ")
            link = personLinks[index]

            """
            stemmer = stem.CroatianStemmer()   
            cleanTextParser = ctp.CleanText()
            articleText = cleanTextParser.getOneArticleText(link)
            articleText = articleText.split(" ")
            articleText = [wordText.strip(".").strip(",").strip("'").strip(":").strip(";").strip("-").strip("!").strip("?").strip("+").strip("").strip("(").strip(")").strip("/") for wordText in articleText]
            articleText = [wordText.lower() for wordText in articleText]
            articleText = [stemmer.stemOneWord(wordText) for wordText in articleText]
            articleText = [wordText for wordText in articleText if wordText is not None]
            """
            
            for person in allPersonFromDBInfo:
                
                idPerson = person[0] 
                #stemmedName = stemmer.stemOneWord(person[1].lower())
                stemmedSurname = ""
                surname = person[2].split(" ")
                for s in surname:
                    stemmedSurname += stemmer.stemOneWord(s.lower()) + " "
                stemmedSurname.strip(" ")
                tags = person[3]
                
                partsurname = stemmedSurname.split(" ")
                for ps in partsurname:
                    if(ps in sentence):
                        #if(stemmedName in articleText):
                            if ((stemmedSurname, link, idPerson) in listOfFoundPerson):
                                listOfFoundPerson[(stemmedSurname, link, idPerson)].append(tags)
                            else:
                                listOfFoundPerson[(stemmedSurname, link, idPerson)] = [tags]                  
            index += 1

        print (listOfFoundPerson)
    
        listOfPersonSaveToDB = []
        for key in listOfFoundPerson:
            # MULTIPLE PERSON WITH SAME SURNAME (ID OF PERSON) !!! (SURNAME NOT UNIQUE IN DB)
            surname = key[0]
            link = key[1].strip("\n")
            idP = key[2]
            print (link)
            #print (key)
            tags = listOfFoundPerson[key]
            rightPersonCounter = 0
            maxTag = ""
            for tag in tags:
                rightPersonCounter = max(rightPersonCounter, self.compareArticleTextWithDBTag(tag, link))
                maxTag = tag
            if(rightPersonCounter > 1):
                listOfPersonSaveToDB.append((surname, link, maxTag, idP))
        return listOfPersonSaveToDB
    
    
    
        
    # COMPARE TEXT OF ARTICLE WITH TAGS FROM DB TO FIND RIGHT PERSON FROM DB (person with same surname...)
    # FROM LINK WE GET ARTICLE AND COMPARE TAG WITH IT
    # RETURN NUMBER OF APPEARENCES OF TAG-WORDS FOR THAT LINK (ARTICLE)
    def compareArticleTextWithDBTag(self, tag, link):
        
        stemmer = stem.CroatianStemmer()   
        cleanTextParser = ctp.CleanText()
        articleText = cleanTextParser.getOneArticleText(link)
        tag = tag.split("-")
        articleText = articleText.split(" ")
        counter = 0
        #print (link)
        listCounter = []
        for wordText in articleText:
            wordText = wordText.strip(".").strip(",").strip("'").strip(":").strip(";").strip("-").strip("!").strip("?").strip("+").strip("").strip("(").strip(")").strip("/")
            for wordTag in tag:                
                if (stemmer.stemOneWord(wordText) != None and stemmer.stemOneWord(wordTag) != None):
                    if(stemmer.stemOneWord(wordText.lower()) == stemmer.stemOneWord(wordTag.lower())):
                        if (wordTag not in listCounter):
                            listCounter.append(wordTag)
                            counter += 1
                            #print (wordText, wordTag)
        return counter
    
        

    # GET LIST OF ALL PERSONS FROM DB
    def getPersonFromDB(self):
        
        db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="root",
                     db="personpublicinfo",
                     charset='utf8',
                     use_unicode=True)

        cur = db.cursor()
        cur.execute("SELECT * FROM person")
        listOfAllpersonsBD = []
        for row in cur.fetchall():
            #print (row)
            listOfAllpersonsBD.append(row)
        db.close()
        return listOfAllpersonsBD

    

    # SAVE PERSON INFO (ID AND LINK) TO DB    
    def savePersonInfoToDB(self, personInfo, publishingDate, imageArticle):  
        
        # make connection to my database
        db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="root",
                     db="personpublicinfo",
                     charset='utf8',
                     use_unicode=True)
        cur = db.cursor()
        
        
        # get data to be used when searching DB
        _surname = personInfo[0]
        link = personInfo[1]
        tag = personInfo[2]
        idP = personInfo[3]
        
        # find right person by surname and tags (person with same surname !!!)
        cur.execute('SELECT * FROM person WHERE id = %s AND tags = %s', (int(idP), tag))
        
        # get person with SQL statement from above
        personFromDB = cur.fetchone()
        personID = personFromDB[0]
        
        #print (personID, link)
        
        # find index of last row in DB
        cur.execute('SELECT * FROM personinfo ORDER BY id DESC LIMIT 1;')
        maxid = cur.fetchone()
        if (maxid == None):
            maxid = 0
        else:
            maxid = maxid[0]
            
        # insert personid and link into DB personinfo table
        cur.execute('INSERT INTO personinfo (id, personid, link, datePub, image) VALUES (%s, %s, %s, %s, %s)', (int(maxid + 1), int(personID), link, publishingDate, imageArticle))
        db.commit()            
        db.close()

  
        
    def getPersonInfoFromDB(self, link, publishingDate, imageArticle):        
        # make connection to my database
        db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="root",
                     db="personpublicinfo",
                     charset='utf8',
                     use_unicode=True)
        cur = db.cursor()
        
        # find index of last row in DB
        cur.execute('SELECT * FROM personinfo WHERE link = %s AND datePub = %s AND image = %s', (link, publishingDate, imageArticle))
        db.commit() 
        result = cur.fetchone()
        print ("aaaaaaaaaaaaaaa\n")
        print (link)
        print (result)  
        db.close()
        return result