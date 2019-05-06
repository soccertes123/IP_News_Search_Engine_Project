import sys
import re
import pandas as pd
import csv
from string import punctuation
import pickle
from porterStemmer import PorterStemmer
from collections import defaultdict
from array import array
import gc

porter=PorterStemmer()

class CreateIndex:

	def __init__(self, stopwordsfile, corpusfile, indexfile):
		self.stopWords_file = stopwordsfile
		self.corpus_file = corpusfile
		self.index_file = indexfile
		self.index = defaultdict(list) # inverted index

	def storeStopwords(self):
		# stopwords function influenced by http://www.ardendertat.com/2011/05/30/how-to-implement-a-search-engine-part-1-create-index/
		with open(self.stopWords_file, 'r') as f:
			stop_word_list = [line.rstrip('\n') for line in f]
			self.stopword_list = stop_word_list

	def createIndex(self):
		# creates an inverse index out of a dictionary to represent word positions in documents
		corp = pd.read_csv(self.corpus_file, encoding = "mac_roman")
		for i, body in enumerate(corp['body']):
			# combine title and body of document
			txt = corp['title'][i] + " " + body
			# now get rid of punctuation and case
			txt = ''.join(c for c in txt if c not in punctuation)
			txt = txt.lower()
			wordList = txt.split()
			
			# create a temporary dictionary for words in the document
			tempDict = defaultdict(list)
			position = 0
			for word in wordList:
				w = porter.stem(word, 0, len(word)-1)
				if w not in self.stopword_list:
					try:
						tempDict[w][1].append(position)
					except:
						tempDict[w] = [corp['id'][i], [position]]
					position += 1
			self.mergeIndex(tempDict)
		self.saveIndexToFile()

	def mergeIndex(self, localDict):
		# merges the index with a subindex
		for word in localDict:
			self.index[word].append(localDict[word])
	
	def saveIndexToFile(self):
		# saves the index to a pickle file so that it can be loaded later
		pickle_out = open(self.index_file,"wb")
		pickle.dump(self.index, pickle_out)
		pickle_out.close()
	
	def loadIndexFromFile(self):
		# load the pickle file into the index variable
		pickle_in = open(self.index_file, "rb")
		self.index = pickle.load(pickle_in)

if __name__=="__main__":
	c=CreateIndex("stopwords.dat", "testCorpus.csv", "testIndex.pickle")
	c.storeStopwords()
	c.createIndex()
	# c.loadIndexFromFile()
	# for key, value in c.index.items():
	# 	print(key)
