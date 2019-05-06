import sys
import pickle
from collections import defaultdict


class NgramTable:
    def __init__(self, corp, tb):
        self.table = defaultdict(int)
        self.table_file = tb
        self.corpus = corp

    def createTable(self, gram):
        # creates the ngram table as a dictionary in form of {phrase: count}, where n=gram
        with open(self.corpus) as f:
            contentList = f.readlines()
            for line in contentList:
                li = line.split(":")
                self.addToTable(li[2], li[1], gram)
        return

    def addToTable(self, phrase, amount, gram):
        # adds segments of the phrase to the gram table based off of how many grams are passed in
        li = []
        wordList = phrase.split()
        if (len(wordList) < gram):
            s = ""
            for word in wordList:
                s += word + " "
            li.append(s[:-1])
            if (s[:-1 in self.table]):
                self.table[s[:-1]] += amount
            else:
                self.table[s[:-1]] = amount
        else:
            for i in range(0, len(wordList)-gram+1):
                s = ""
                for k in range(i, i+gram):
                    s += wordList[k] + " "
                if (s[:-1 in self.table]):
                    self.table[s[:-1]] += amount
                else:
                    self.table[s[:-1]] = amount
        return

    def saveIndexToFile(self):
        # saves the table to a pickle file so that it can be loaded later
        pickle_out = open(self.table_file,"wb")
        pickle.dump(self.table, pickle_out)
        pickle_out.close()
	
    def loadIndexFromFile(self):
        # load the pickle file into the index variable
        pickle_in = open(self.table_file, "rb")
        self.table = pickle.load(pickle_in)

if __name__ == "__main__":
    c = NgramTable("queries.txt", "ngram_table.pickle")
    c.createTable(4)
    