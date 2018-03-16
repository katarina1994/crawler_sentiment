'''
Created on 17. pro 2017.

@author: Katarina123
'''

import urllib
import codecs
import spiders.linkParser as linkParser
import re

# crawl web pages, starting from given link
# parameters: url - link of starting web page
#             maxPages - number of pages to reach in depth
#             domain - domain of web page to be crawled
#             f_all - file for writing all crawled links
# return: NONE
def spider(url, domain, regexExpr, maxPages, fAll): 
    
    visited = []
    pagesToVisit = [url]
    numberVisited = 0
    
    while numberVisited < maxPages and pagesToVisit != []:
        
        #numberVisited = numberVisited + 1
        #print ("NUMBER OF VISITED PAGES: " + str(numberVisited))
        url = pagesToVisit[0]
        pagesToVisit = pagesToVisit[1:]
       
        try:
            parser = linkParser.LinkParser()
            data, links = parser.getLinks(url)
            
            #if regexExpr in data:
            if re.match(regexExpr, url, flags=0):
                fAll.write(url + "\n")
                f = codecs.open("webPagesHTML/web-page-%d.txt" % numberVisited, 'w', encoding='Windows-1250')
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
