'''
Created on 12. sij 2018.

@author: Katarina123
'''

import re
import codecs
import urllib
from urllib.request import urlopen  
from bs4 import BeautifulSoup as bs
#from bs4.element import Comment
import CroatianStemmer.Croatian_stemmer as stem
#from sentiment import cataloguePersonHelper
from polyglot.text import Text



class CleanText():
    
    def writeCleanTextAndTitlesFromHtmlToFile(self, path, numberOfLinks, numberOfPages):  
        
        # get all articles' text
        cleanTextsArticles = self.getAllArticlesText(path, numberOfLinks, numberOfPages)
                
        index = numberOfLinks - numberOfPages
        for article in cleanTextsArticles:
            fClean = codecs.open("cleanTextFromHTML/clean-web-page-%05d.txt" % index, 'w', encoding='Windows-1250')
            fClean.write(article.encode('Windows-1250', 'replace').decode('Windows-1250', 'replace'))
            fClean.close()     
            index += 1       
                
        # write titles to file
        self.writeAllArticlesTitlesToFile(path, numberOfLinks - numberOfPages)
        
    def getTextFromHtml(self, html):
        
        soup = bs(html, 'html.parser')
        #texts = soup.findAll('p', attrs={'class': None})
        #texts += soup.findAll('div', attrs={})  
        texts = ""
        # Get rid of comments below articles
        commentSection = ""
        #comment = soup.findAll('div', class_ = 'nickname')
        for tag in soup.select('div[class*="comment"]'):
            commentSection += tag.text
        for tag in soup.select('span[class*="comment"]'):
            commentSection += tag.text
        for tag in soup.select('p[class*="comment"]'):
            commentSection += tag.text
        
        for tag in soup.findAll('p'):
            if (tag.text not in commentSection and (tag.attrs == {} or tag.attrs == {'sytle'} or tag.attrs == {'align'}) and not tag.find('script')):
                texts += tag.text
                texts += " "
                
        for tag in soup.findAll('div'):
            if (tag.text not in commentSection and (tag.attrs == {} or tag.attrs == {'sytle'} or tag.attrs == {'align'}) and not tag.find('script')):
                texts += tag.text
                texts += " "
                
        sentencesOfText = ""
        listOfText = texts.split(". ")
        for partOfText in listOfText:
            #print (partOfText + ".")
            tmp = ""
            tmp = partOfText + ". "
            sentencesOfText += tmp
        return sentencesOfText.replace('\n', '').replace('\r', '').replace('\t', '')
        #return texts.replace('\n', '').replace('\r', '').replace('\t', '')



    def getTitleFromHtml(self, html):
        
        soup = bs(html, 'html.parser')
        for tag in soup.findAll('title'):
            return tag.text
        
        
    def getAllArticlesText(self, path, numberOfLinks, numberOfPages):
        
        fHtml = codecs.open(path, 'r', encoding='Windows-1250')
        links = fHtml.readlines()
        listOfArticles = []
        numberOfLinks = numberOfLinks - numberOfPages
        
        while (numberOfLinks < len(links)):
            html = ""
            try:
                html = urlopen(links[numberOfLinks]).read()
            except urllib.error.HTTPError as e:
                html = "404 NOT FOUND"
                print(e)
            cleanTexts = self.getTextFromHtml(html)
            cleanTexts = cleanTexts.strip(" ").strip("\t").strip("\n").strip("\r").strip()
            listOfArticles.append(cleanTexts)
            numberOfLinks += 1        
        fHtml.close()
               
        return listOfArticles

    def getOneArticleText(self, link):      
        
        html = urlopen(link).read()
        cleanTexts = self.getTextFromHtml(html)
        cleanTexts = cleanTexts.strip(" ").strip("\t").strip("\n").strip("\r").strip()
        return cleanTexts


    def writeAllArticlesTitlesToFile(self, path, numberOfLinks):
        
        fHtml = codecs.open(path, 'r', encoding='Windows-1250')
        fTitles = codecs.open("allTitles.txt", 'a', encoding='Windows-1250')

        links = fHtml.readlines()
        
        while (numberOfLinks < len(links)): 
            html = urlopen(links[numberOfLinks]).read()
            title = self.getTitleFromHtml(html)
            fTitles.write((title.replace("\n", "") + "\n").encode('Windows-1250', 'replace').decode('Windows-1250', 'replace'))     
            numberOfLinks += 1        

        fHtml.close()
        fTitles.close()




    def getAllTitlesOfArticles(self, topicNumber, numberOfPages):

        stemmer = stem.CroatianStemmer()        
        start = topicNumber - numberOfPages
        end =  topicNumber
        fTitles = codecs.open("allTitles.txt", 'r')
        allTitles = fTitles.readlines()[start:end]
        allTitles = [title.lower().strip().strip(" ").strip("\n").strip("\t").strip("\r") for title in allTitles]
        allTitles = [oneTitle.split(" ") for oneTitle in allTitles]
        allTitles = [[word.strip(".").strip(",").strip("'").strip(":").strip(";").strip("-").strip("!").strip("?").strip("+").strip("").strip("(").strip(")").strip("/") for word in oneTitle] for oneTitle in allTitles]
        allTitles = [[word for word in oneTitle if word is not ""] for oneTitle in allTitles]
        allTitles = [[stemmer.stemOneWord(word) for word in oneTitle] for oneTitle in allTitles]
        allTitles = [[word for word in oneTitle if word is not None] for oneTitle in allTitles]        
        allTitles = [Text(" ".join(oneTitle), hint_language_code='hr').sentences[0] for oneTitle in allTitles]
        fTitles.close()
        
        return allTitles
    
    def getPolyglotSentenceList(self, listOfWords):
        
        listPoly = []
        listOfWordsPoly = Text(" ".join(listOfWords), hint_language_code='hr')
        if (listOfWordsPoly):
            listPoly.append(listOfWordsPoly.sentences[0]) 
        else:
            listPoly.append("-")
        return listPoly
    
    
    def getDateFromURL(self, link):
        
        html = urlopen(link).read()
        html = html.decode("utf-8") 
        dateRegex = re.compile("\d{4}-\d\d-\d\dT")
        matchedDates = re.findall(dateRegex, html)
        return matchedDates[0].rstrip("T")
        
        
    def getImageOfArticle(self, link):
        
        html = urlopen(link).read()
        soup = bs(html, 'html.parser')
        image = soup.find("meta",  property="og:image")
        if(image):
            return image["content"]
        else:
            return "No image to display!"