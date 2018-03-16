'''
Created on 9. sij 2018.

@author: Katarina123
'''


from html.parser import HTMLParser 
from urllib.request import urlopen  
from urllib import parse


class LinkParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    newUrl = parse.urljoin(self.baseUrl, value)
                    self.links = self.links + [newUrl]


    def getLinks(self, url):
        self.links = []
        self.baseUrl = url
        response = urlopen(url)
        #print (response.info().get('Content-Type'))

        if ('text/html' in response.info().get('Content-Type')):
            htmlBytes = response.read()
            try:
                htmlString = htmlBytes.decode('utf-8')
            except UnicodeDecodeError:
                htmlString = ""
                pass
            
            self.feed(htmlString)
            return htmlString, self.links
        else:
            return "",[]