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

class Query:

	def __init__(self):
		self.stopWords_file = "stopwords.dat"
		self.corpus_file = "testCorpus.csv"
		self.index_file = "testIndex.pickle"
		self.index=defaultdict(list) # inverted index

	def storeStopwords(self):
		# stopwords function influenced by http://www.ardendertat.com/2011/05/30/how-to-implement-a-search-engine-part-1-create-index/
		with open(self.stopWords_file, 'r') as f:
			stop_word_list = [line.rstrip('\n') for line in f]
			self.stopword_list = stop_word_list
	
	def loadIndexFromFile(self):
        # load the pickle file into the index variable
		pickle_in = open(self.index_file,"rb")
		self.index = pickle.load(pickle_in)

	def getRelevantDocuments(self, query):
		query = ''.join(c for c in query if c not in punctuation)
		query = query.lower()
		# performs a phrase query to return relevant documents that have the exact query within the document
		# will return this list containing relevant docs later
		relevantDocs = []
		# whichDocs contains a list of documents for each word where the word appears in the document
		whichDocs = defaultdict(list)
		queryList = []
		for word in query.split():
			w = porter.stem(word, 0, len(word)-1)
			if w not in self.stopword_list:
				queryList.append(w)
				if w in self.index:
					whichDocs[w] = []
					for doc in self.index[w]:
						# add the document id to the list containing which documents the word appears in
						whichDocs[w].append(doc[0])
				else:
					# query word doesn't exist in index
					return []
		if not whichDocs:
			return None
		# intersectionList will be the list of documents that contain all query terms
		intersectionList = list(whichDocs.values())[0]
		for docList in list(whichDocs.values()):
			intersectionList = self.intersection(intersectionList, docList)
		for docId in intersectionList:
			# for each relevent document, get a dictionary corresponding query words to their positions in the document
			qWordPositions = [None] * len(queryList)
			for i, qWord in enumerate(queryList):
				w = porter.stem(qWord, 0, len(qWord)-1)
				for documents in self.index[w]:
					if (documents[0] == docId):
						# put the list of word positions into the appropriate bucket
						decrementPositionList = []
						for position in documents[1]:
							# subtracting i from the word's position will allow us to compare proximity between words later by intersecting lists
							decrementPositionList.append(position - i)
						qWordPositions[i] = decrementPositionList
			testIntersection = qWordPositions[0]
			for li in qWordPositions:
				testIntersection = self.intersection(testIntersection, li)
			if testIntersection:
				# document has a match for the query; add it to the relevant documents list
				relevantDocs.append(docId)
		return relevantDocs

	def intersection(self, list1, list2):
		# got this trick from https://www.geeksforgeeks.org/python-intersection-two-lists/
		return set(list1).intersection(list2)

if __name__=="__main__":
	q=Query()
	q.storeStopwords()
	q.loadIndexFromFile()
	query = input("Enter a query: ")
	relevantDocuments = q.getRelevantDocuments(query)
	if not relevantDocuments:
		print("Couldn't find any documents to match your query")
	else:
		corp = pd.read_csv(q.corpus_file, encoding = "mac_roman")
		for id in relevantDocuments:
			# print out relevant titles
			print(corp['title'][id-1])
			txt = corp['title'][id-1] + " " + corp['body'][id-1]