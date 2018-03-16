'''
Created on 9. sij. 2018.

@author: Katarina123
'''

import codecs
import spiders.myFirstSpider as sp
import spiders.roundRobinSpider as rrsp
import spiders.cleanTextParser as ctp



#REGULAR SPIDER
fConfig = open("configurationFiles/config.txt", "r");
domain = fConfig.readline().strip("\n")
regexExpr = fConfig.readline().strip("\n")
numberOfPages = fConfig.readline()

fAll = codecs.open("allLinks.txt", 'w', encoding='Windows-1250')
sp.spider("https://" + domain, domain, regexExpr, int(numberOfPages), fAll)
fAll.close()



"""
#ROUDN ROBIN
domains = []
regexExpressions = []
howManyPagesToCrawl = 0

f_RRconfig = open("configurationFiles/roundRobinConfig.txt", "r");
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

fAll = codecs.open("allLinks.txt", 'w', encoding='Windows-1250')
links = rrsp.roundRobinSpider(pagesToVisit, domains, regexExpressions, howManyPagesToCrawl, fAll)
fAll.close()
   
"""
    
cleanTextParser = ctp.CleanText()
cleanTextParser.getCleanTextFromHtml()