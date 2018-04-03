#!/usr/bin/env python
# -*- coding: Windows-1250 -*-

#
#    Simple stemmer for Croatian v0.1
#    Copyright 2012 Nikola Ljubešić and Ivan Pandžić
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
import sys
import glob
import os
import codecs



def istakniSlogotvornoR(niz):
	return re.sub(r'(^|[^aeiou])r($|[^aeiou])',r'\1R\2',niz)

def imaSamoglasnik(niz):
	if re.search(r'[aeiouR]',istakniSlogotvornoR(niz)) is None:
		return False
	else:
		return True

def transformiraj(pojavnica):
	for trazi,zamijeni in transformacije:
		if pojavnica.endswith(trazi.encode('Windows-1250')):
			return pojavnica[:-len(trazi.encode('Windows-1250'))]+zamijeni.encode('Windows-1250')
	return pojavnica

def korjenuj(pojavnica):
	for pravilo in pravila:
		dioba=pravilo.match(pojavnica)
		if dioba is not None:
			if imaSamoglasnik(dioba.group(1)) and len(dioba.group(1))>1:
				return dioba.group(1)
	return pojavnica
	
if __name__=='__main__':
	if len(sys.argv)!=3:
		print 'Usage: python Croatian_stemmer.py input_file output_file'
		print 'input_file should be an utf8-encoded text file which is then tokenized, stemmed and written in the output_file in a tab-separated fashion.'
		sys.exit(1)
		
		
	# CREATE SET OF STOPWORDS
	#stop=set(['biti','jesam','budem','sam','jesi','bude�','si','jesmo','budemo','smo','jeste','budete','ste','jesu','budu','su','bih','bijah','bjeh','bija�e','bi','bje','bje�e','bijasmo','bismo','bjesmo','bijaste','biste','bjeste','bijahu','biste','bjeste','bijahu','bi','bi�e','bjehu','bje�e','bio','bili','budimo','budite','bila','bilo','bile','�u','�e�','�e','�emo','�ete','�elim','�eli�','�eli','�elimo','�elite','�ele','moram','mora�','mora','moramo','morate','moraju','trebam','treba�','treba','trebamo','trebate','trebaju','mogu','mo�e�','mo�e','mo�emo','mo�ete'])
	path = "C:/Users/Katarina123/workspace/textChanges/textCroatian/stopWords.txt"
	f = codecs.open(path, 'r', encoding='Windows-1250')
	stop = set()
	for line in f.readlines():
		stop.add(line.strip("\n"))
	f.close()
	#print stop
	
	#output_file=open(sys.argv[2],'w')
	pravila=[re.compile(r'^('+osnova+')('+nastavak+r')$') for osnova, nastavak in [e.decode('Windows-1250').strip().split(' ') for e in open('rules.txt')]]
	transformacije=[e.decode('Windows-1250').strip().split('\t') for e in open('transformations.txt')]
	path = sys.argv[1]
	numberOfLink = 0
	for fileName in glob.glob(os.path.join(path, '*.txt')):
		output_file = open("stemmedWords/stemmed-web-page-%d.txt" % numberOfLink, 'w')
		for token in re.findall(ur'[\u0041-\u017F]+',open(fileName).read(),re.UNICODE):
			if token.lower() in stop:
				output_file.write(token + "\n")
				#output_file.write((token+'\t'+token.lower()+'\n').encode('utf8'))
				continue
			#output_file.write((token+'\t'+korjenuj(transformiraj(token.lower()))+'\n'))
			#print (token)
			if(" " not in token):
				output_file.write(token + " " + korjenuj(transformiraj(token)) + "\n")

		output_file.close()
		numberOfLink += 1
