'''
Created on 12. sij 2018.

@author: Katarina123
'''

import codecs
from urllib.request import urlopen  
from bs4 import BeautifulSoup as bs
#from bs4.element import Comment


class CleanText():
    
    def getCleanTextFromHtml(self):  
        f_html = codecs.open("C:/Users/Katarina123/workspace/mainProject/mainPackage/allLinks.txt", 'r', encoding='Windows-1250')
        links = f_html.readlines()
        numberOfLink = 0
        for link in links:
            #print(link)
            html = urlopen(link).read()
            cleanTexts = self.textFromHtml(html)
            cleanTexts = cleanTexts.strip(" ").strip("\t").strip("\n").strip("\r").strip()
            f_clean = codecs.open("C:/Users/Katarina123/workspace/mySpider/spiders/cleanTextFromHTML/clean-web-page-%05d.txt" % numberOfLink, 'w', encoding='Windows-1250')
            f_clean.write(cleanTexts.encode('Windows-1250', 'replace').decode('Windows-1250', 'replace'))
            f_clean.close()
            numberOfLink += 1
        f_html.close()
        
    def textFromHtml(self, html):
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
            if (tag.text not in commentSection and (tag.attrs == {} or tag.attrs == {'sytle'}) and not tag.find('script')):
                texts += tag.text
                texts += " "
                
        for tag in soup.findAll('div'):
            if (tag.text not in commentSection and (tag.attrs == {} or tag.attrs == {'sytle'}) and not tag.find('script')):
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
