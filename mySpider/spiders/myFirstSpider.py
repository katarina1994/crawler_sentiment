'''
Created on 17. pro 2017.

@author: Katarina123
'''

import urllib
import codecs
import spiders.linkParser as linkParser
import re


class RegularSpider():
    # crawl web pages, starting from given link
    # parameters: url - link of starting web page
    #             maxPages - number of pages to reach in depth
    #             domain - domain of web page to be crawled
    #             f_all - file for writing all crawled links
    # return: NONE
    def spider(self, url, domain, regexExpr, maxPages, fAll, numberVisited): 
        
        visited = []
        pagesToVisit = [url]
        #print (numberVisited, maxPages)
        maxCrawl = maxPages + numberVisited
        
        while (numberVisited < maxCrawl and pagesToVisit != []):
            
            #numberVisited = numberVisited + 1
            #print ("NUMBER OF VISITED PAGES: " + str(numberVisited))
            url = pagesToVisit[0]
            pagesToVisit = pagesToVisit[1:]
        
            try:
                parser = linkParser.LinkParser()
                data, links = parser.getLinks(url)
                
                fAll.seek(0)
                allLines = fAll.readlines()
                allLines = [line.strip("\n") for line in allLines]

                #fAll.seek(0)
                #if regexExpr in data:
                if re.match(regexExpr, url, flags=0):                  
                    if url not in allLines:
                        print (url)
                        #fAll.seek(2)
                        fAll.write(url + "\n")
                        f = codecs.open("webPagesHTML/web-page-%05d.txt" % numberVisited, 'w', encoding='Windows-1250')
                        f.write(data.encode('Windows-1250', 'replace').decode('Windows-1250', 'replace'))
                        f.close()
                        numberVisited = numberVisited + 1
                #time.sleep(10)
                tmp = []
                for link in links:               
                    if (domain in link) and (link not in visited):
                        tmp.append(link)
                        visited.append(link)
                        #print (link)
                        
                links = tmp
                pagesToVisit += links
        
            except urllib.error.URLError as e:
                print("FAIL due to following error: " + str(e))          
