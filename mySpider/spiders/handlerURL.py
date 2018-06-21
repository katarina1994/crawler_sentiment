'''
Created on 9. sij 2018.

@author: Katarina123
'''


from html.parser import HTMLParser 
from urllib.request import urlopen  
from urllib import parse


class handlerURL (HTMLParser):

    def handle_starttag(self, tag, attrs):
        if (tag == "a"):
            for (key, value) in attrs:
                if (key == "href"):
                    newUrl = parse.urljoin(self.start, value)
                    listOfURL = [newUrl]
                    self.links = self.links + listOfURL


    def getURLs(self, url):
        self.links = []
        self.start = url
        result = urlopen(url.encode('ascii', 'ignore').decode('ascii'))
        #print (response.info().get('Content-Type'))

        contentType = result.info().get("Content-Type")
        if ("text/html" in contentType):
            htmlInByte = result.read()
            try:
                htmlStr = htmlInByte.decode('utf-8')
            except UnicodeDecodeError:
                htmlStr = ""
                pass
            
            self.feed(htmlStr)
            return (htmlStr, self.links)
        else:
            return ("", [])