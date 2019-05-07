import sys
import pickle
import math
from string import punctuation

class Ngrams:

    def __init__(self, q, tablefile):
        q = ''.join(c for c in q if c not in punctuation)
        q = q.lower()
        self.query = q
        self.table_file = tablefile
        self.loadIndexFromFile()
        self.total = self.totalCount()

    def predict(self, grams, topX):
        # predicts the next word based on the number of grams we want to check; returns list of topX words in descending order
        # count how many times this query has occurred
        # nextWordList gets all of the next possible words based on the query
        nextWordList = self.getNextWords()
        # probMatrix will hold the probabilities for each of the next possible words
        probMatrix = [1] * len(nextWordList)
        for i, word in enumerate(nextWordList):
            # for each word, calculate probability and store in probMatrix
            probability = self.getProbability(word, grams)
            probMatrix[i] = probability
        # return the top 5 words
        return self.topList(probMatrix, nextWordList, topX)

    # ************************************ TO IMPLEMENT ************************************
    def getNextWords(self):
        # given a query, returns a list of the possible next words that could occur based on our index
        li = []
        qLen = len(self.query)
        for key, value in self.table.items():
            if self.query == key[:qLen] and key[qLen:] != '':
                # make sure that query matches the key but there is still more words in the key
                if key[qLen] == ' ':
                    # get rid of first space
                    if len(key) > qLen+1:
                        # Don't want index out of bounds error
                        li.append(key[qLen+1:])
                else:
                    li.append(key[qLen:])
        return li

    # ************************************ TO IMPLEMENT ************************************
    def getProbability(self, nextWord, grams):
        # returns probability of nextWord based on query
        # grams is the amount of grams for our model
        queryList = self.query.split()
        window = []
        if len(queryList) > 1:
            for i in range(len(queryList)-grams, len(queryList)):
                window.append(queryList[i])
        elif len(self.query) > 0:
            window.append(queryList[0])
        countQuery = self.getFrequency(queryList)
        queryList.append(nextWord)
        countNext = self.getFrequency(queryList)
        return float(math.log(countNext)+1)/float(math.log(countQuery)+1)

    def getFrequency(self, wordList):
        # given a list of words, returns a count of how many times a phrase occurred in that order from the corpus
        if (len(wordList) == 0):
            return self.total
        s = ""
        for word in wordList:
            s += word + " "
        s = s[:-1]
        return int(self.table[s])
    
    def totalCount(self):
        # returns the total amount of query data
        total = 0
        for key, value in self.table.items():
            total += int(value)
        return total

    def topList(self, probMatrix, nextWordList, n):
        # returns the top n words in descending order based on the probability matrix
        ret = []
        for i in range(0, n):
            maxVal = 0
            maxIndex = 0
            for k, val in enumerate(probMatrix):
                if val > maxVal:
                    maxVal = val
                    maxIndex = k
            ret.append(nextWordList[maxIndex])
            probMatrix[maxIndex] = 0
        return ret

    def loadIndexFromFile(self):
        # load the pickle file into the index variable
        pickle_in = open(self.table_file, "rb")
        self.table = pickle.load(pickle_in)


if __name__=="__main__":
    q = input("Enter the first part of your query: ")
    n = Ngrams(q, "ngram_table.pickle")
    print(n.predict(4, 5))