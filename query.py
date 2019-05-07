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

	def __init__(self, stopwordsfile, corpusfile, picklefile):
		self.stopWords_file = stopwordsfile
		self.corpus_file = corpusfile
		self.index_file = picklefile
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

class Test:
	def __init__(self, queryfile, queryobject):
		# constructor
		self.queryFile = queryfile
		self.QueryObj = queryobject
		# correctDocs will hold the correct documents to retrieve for a given query
		self.correctDocs = defaultdict(list)
		self.retrievedDocs = defaultdict(list)
		corp = pd.read_csv(self.queryFile, encoding = "mac_roman")
		for i, query in enumerate(corp['query']):
			strDocs = corp['documents'][i]
			liStrDocs = strDocs.split(',')
			liDocs = []
			for id in liStrDocs:
				liDocs.append(int(id))
			# add the list of correct documents to the dictionary
			self.correctDocs[query] = liDocs
			self.retrievedDocs[query] = queryobject.getRelevantDocuments(query)
    
	def testPrecision(self):
		listOfPrecisions = []
		for query, docs in self.correctDocs.items():
			# avoid divide by zero errors
			if len(self.retrievedDocs[query]) != 0:
				intersection = self.QueryObj.intersection(docs, self.retrievedDocs[query])
				# precision is the amount of correctly returned docs divided by the amount of docs that were returned
				listOfPrecisions.append(float(len(intersection))/float(len(self.retrievedDocs[query])))
		# take the average precision and return it
		avgPrecision = 0.0
		for prec in listOfPrecisions:
			avgPrecision += prec
		return avgPrecision/float(len(listOfPrecisions))

	def testRecall(self):
		listOfRecalls = []
		for query, docs in self.correctDocs.items():
			# avoid divide by zero errors
			if len(docs) != 0:
				intersection = self.QueryObj.intersection(docs, self.retrievedDocs[query])
				# recall is the amount of correctly returned docs divided by the amount of docs that should have been returned
				listOfRecalls.append(float(len(intersection))/float(len(docs)))
		# take the average recall and return it
		avgRecall = 0.0
		for rec in listOfRecalls:
			avgRecall += rec
		return avgRecall/float(len(listOfRecalls))

if __name__=="__main__":
	q=Query("stopwords.dat", "testCorpus.csv", "testIndex.pickle")
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
	# qTest will be the query object used to test precision and recall with our sample test data
	qTest=Query("stopwords.dat", "precision_recall_test_corpus.csv", "testIndex.pickle")
	qTest.storeStopwords()
	qTest.loadIndexFromFile()
	t = Test("testQueries.csv", qTest)
	print("precision: ", t.testPrecision())
	print("recall: ", t.testRecall())