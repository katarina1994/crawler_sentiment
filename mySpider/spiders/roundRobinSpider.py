'''
Created on 19. sij 2018.

@author: Katarina123
'''

import urllib
import codecs
import spiders.handlerURL as handURL
from random import randint
import re


class RoundRobinSpider():
    # crawl web pages, starting from given link
    # parameters: url - link of starting web page
    #             maxPages - number of pages to reach in depth
    #             domain - domain of web page to be crawled
    #             f_all - file for writing all crawled links
    # return: NONE
    # FIX ME !!!!!!!!!!!!!!!!!
    def roundRobinSpider(self, pagesToVisit, domains, regexExpressions, howManyPagesToCrawl, fAll, numberVisited): 
            
            visited = []
            maxCrawl = howManyPagesToCrawl + numberVisited
            while (numberVisited < maxCrawl):
                
                #which page will we crawl?
                whichDomain = randint(0, len(domains)-1)
                pickedDomain = domains[whichDomain]
                
                #pick one of links from pages that belong to picked domain
                number = randint(0, len(pagesToVisit)-1)
                while pickedDomain not in pagesToVisit[number]:
                    number = randint(0, len(pagesToVisit)-1)
                url = pagesToVisit[number]
                
                try:
                    handler = handURL.handlerURL()
                    #print("URL: " + url)
                    data, links = handler.getURLs(url)
                    fAll.seek(0)
                    allLines = fAll.readlines()
                    allLines = [line.strip("\n") for line in allLines]
                    
                    for regexExpr in regexExpressions:
                        #print (data)
                        if re.match(regexExpr, url, flags=0):
                            #print("URL that crawler found as target: " + url)
                            if url not in allLines:
                                fAll.write(url + "\n")
                                f = codecs.open("webPagesHTML/web-page-%05d.txt" % numberVisited, 'w', encoding='Windows-1250')
                                f.write(data.encode('Windows-1250', 'replace').decode('Windows-1250', 'replace'))
                                f.close()
                                numberVisited += 1
                    tmp = []
                    if links:
                        for link in links:   
                            for domain in domains:          
                                if (domain in link) and (link not in visited):
                                    tmp.append(link)
                                    visited.append(link)
                    links = tmp     
                    pagesToVisit += links
                    #print (pagesToVisit)
                except urllib.error.URLError as e:
                    print("FAIL due to following error: " + str(e))
