#!/usr/bin/env python
# -*- coding: Windows-1250 -*-

#
#    Simple stemmer for Croatian v0.1
#    Copyright 2012 Nikola LjubeĹˇiÄ‡ and Ivan PandĹľiÄ‡
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


import re
import glob
import os
import codecs



class CroatianStemmer():
	
	def __init__(self):
		self.pravila = []
		self.transformacije = []

	def istakniSlogotvornoR(self, niz):
		return re.sub(r'(^|[^aeiou])r($|[^aeiou])',r'\1R\2',niz)
	
	def imaSamoglasnik(self, niz):
		if re.search(r'[aeiouR]',self.istakniSlogotvornoR(niz)) is None:
			return False
		else:
			return True
	
	def transformiraj(self, pojavnica):
		for trazi,zamijeni in self.transformacije:
			if pojavnica.endswith(trazi):
				return pojavnica[:-len(trazi)]+zamijeni
		return pojavnica
	
	def korjenuj(self, pojavnica):
		for pravilo in self.pravila:
			dioba=pravilo.match(pojavnica)
			if dioba is not None:
				if self.imaSamoglasnik(dioba.group(1)) and len(dioba.group(1))>1:
					return dioba.group(1)
		return pojavnica
	
	def stemWords(self):
			
		# CREATE SET OF STOPWORDS
		#stop=set(['biti','jesam','budem','sam','jesi','budeš','si','jesmo','budemo','smo','jeste','budete','ste','jesu','budu','su','bih','bijah','bjeh','bijaše','bi','bje','bješe','bijasmo','bismo','bjesmo','bijaste','biste','bjeste','bijahu','biste','bjeste','bijahu','bi','biše','bjehu','bješe','bio','bili','budimo','budite','bila','bilo','bile','ću','ćeš','će','ćemo','ćete','želim','želiš','želi','želimo','želite','žele','moram','moraš','mora','moramo','morate','moraju','trebam','trebaš','treba','trebamo','trebate','trebaju','mogu','možeš','može','možemo','možete'])
		path = "C:/Users/Katarina123/workspace/textChanges/textCroatian/stopWords.txt"
		f = codecs.open(path, 'r', encoding='Windows-1250')
		stop = set()
		for line in f.readlines():
			stop.add(line.strip("\n"))
		f.close()
		#print stop
		
		#output_file=open(sys.argv[2],'w')
		self.pravila=[re.compile(r'^('+osnova+')('+nastavak+r')$') for osnova, nastavak in [e.strip().split(' ') for e in open('C:/Users/Katarina123/workspace/textCroatianStemmer/CroatianStemmer/rules.txt')]]
		self.transformacije=[e.strip().split('\t') for e in open('C:/Users/Katarina123/workspace/textCroatianStemmer/CroatianStemmer/transformations.txt')]
		path = "C:/Users/Katarina123/workspace/mySpider/spiders/cleanTextFromHTML"
		numberOfLink = 0
		for fileName in glob.glob(os.path.join(path, '*.txt')):
			output_file = open("C:/Users/Katarina123/workspace/textCroatianStemmer/CroatianStemmer/stemmedWords/stemmed-web-page-%05d.txt" % numberOfLink, 'w')
			for token in re.findall(r'[\u0041-\u017F]+',open(fileName).read(),re.UNICODE):
				if token.lower() in stop:
					output_file.write(token + "\n")
					#output_file.write((token+'\t'+token.lower()+'\n').encode('utf8'))
					continue
				#output_file.write((token+'\t'+korjenuj(transformiraj(token.lower()))+'\n'))
				#print (token)
				if(" " not in token):
					output_file.write(token + " " + self.korjenuj(self.transformiraj(token)) + "\n")
		
			output_file.close()
			numberOfLink += 1
