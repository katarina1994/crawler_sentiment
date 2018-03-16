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
        f_html = codecs.open("allLinks.txt", 'r', encoding='Windows-1250')
        links = f_html.readlines()
        numberOfLink = 0
        for link in links:
            #print(link)
            html = urlopen(link).read()
            cleanTexts = self.textFromHtml(html)
            f_clean = codecs.open("cleanTextFromHTML/clean-web-page-%d.txt" % numberOfLink, 'w', encoding='Windows-1250')
            f_clean.write(cleanTexts.encode('Windows-1250', 'replace').decode('Windows-1250', 'replace'))
            f_clean.close()
            numberOfLink += 1
    """
    def tag_visible(self, element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True
    """

    def textFromHtml(self, html):
        soup = bs(html, 'html.parser')
        #texts = soup.findAll('p', attrs={'class': None})
        #texts += soup.findAll('div', attrs={})
        
        
        texts = ""
        for tag in soup.findAll('p'):
            if ((tag.attrs == {} or tag.attrs == {'sytle'}) and not tag.find('script')):
                texts += tag.text
                
        for tag in soup.findAll('div'):
            if ((tag.attrs == {} or tag.attrs == {'sytle'}) and not tag.find('script')):
                texts += tag.text
        
        #visible_texts = filter(self.tag_visible, texts)  
        #return u" ".join(t.strip() for t in visible_texts)
        return texts
