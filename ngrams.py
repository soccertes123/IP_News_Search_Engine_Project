import sys
import pickle
import math
from string import punctuation

class Ngrams:

    def __init__(self, q):
        q = ''.join(c for c in q if c not in punctuation)
        q = q.lower()
        self.query = q
        self.index_file = "testIndex.pickle"

    def predict(self):
        print(self.query)
        # count how many times this query has occurred
        # nextWordList gets all of the next possible words based on the query
        nextWordList = self.getNextWords()
        # probMatrix will hold the probabilities for each of the next possible words
        probMatrix = [1] * len(nextWordList)
        for i, word in enumerate(nextWordList):
            # for each word, calculate probability and store in probMatrix
            probability = self.getProbability(word, 4)
            probMatrix[i] = probability
        maxVal = 0
        maxIndex = 0
        for k, val in enumerate(probMatrix):
            if val > maxVal:
                maxVal = val
                maxIndex = k
        return nextWordList[maxIndex]

    def loadIndexFromFile(self):
        # load the pickle file into the index variable
        pickle_in = open(self.index_file,"rb")
        self.index = pickle.load(pickle_in)

    # ************************************ TO IMPLEMENT ************************************
    def getNextWords(self):
        # given a query, returns a list of the possible next words that could occur based on our index
        li = []
        return li

    # ************************************ TO IMPLEMENT ************************************
    def getProbability(self, nextWord, grams):
        # returns probability of nextWord based on query
        # grams is the amount of grams for our model
        queryList = self.query.split()
        window = []
        for i in range(len(queryList)-grams, len(queryList)-1):
            window.append(queryList[i])
        countQuery = self.getFrequency(queryList)
        queryList.append(nextWord)
        countNext = self.getFrequency(queryList)
        return math.log(countNext)/math.log(countQuery)

    def getFrequency(self, wordList):
        # given a list of words, returns a count of how many times a phrase occurred in that order from the corpus
        return 0

if __name__=="__main__":
    q = input("Enter the first part of your query: ")
    n = Ngrams(q)
    n.loadIndexFromFile()
    n.predict()