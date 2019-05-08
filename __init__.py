from flask import Flask
from flask_cors import CORS
from flask import jsonify
import json
import pandas as pd

from query import Query, Test
from ngrams import Ngrams

app = Flask(__name__)
CORS(app)

@app.route('/query/<input>', methods=['GET'])
def query_app(input):
    # returns the relevant documents for the input query
    q=Query("stopwords.dat", "testCorpus.csv", "testIndex.pickle")
    q.storeStopwords()
    q.loadIndexFromFile()
    relevantDocuments = q.getRelevantDocuments(input)
    # wrap the answer in json format and return ret
    ret = {}
    ret['document'] = []
    if not relevantDocuments:
        print("Couldn't find any documents to match your query")
        documentDict = {}
        ret['document'].append(documentDict)
        json_data = json.dumps(ret)
        return json_data
    else:
        corp = pd.read_csv(q.corpus_file, encoding = "mac_roman")
        for id in relevantDocuments:
            # return out relevant titles
            documentDict = {}
            documentDict['title'] = corp['title'][id-1]
            documentDict['id'] = int(id)
            ret['document'].append(documentDict)
        json_data = json.dumps(ret)
        return json_data

@app.route('/predict_next/<input>', methods=['GET'])
def predict_app(input):
    # this uses ngrams to predict the most likely words that will follow input
    n = Ngrams(input, "ngram_table.pickle")
    # wrap the answer in json format
    ret = {}
    # predict the top 5 words in descending order using 4-grams
    ret['next'] = n.predict(4, 5)
    json_data = json.dumps(ret)
    return json_data

@app.route('/precision_test', methods=['GET'])
def precision_app():
    # returns the precision
    qTest=Query("stopwords.dat", "precision_recall_test_corpus.csv", "testIndex.pickle")
    qTest.storeStopwords()
    qTest.loadIndexFromFile()
    t = Test("testQueries.csv", qTest)
    # wrap the answer in json format
    ret = {}
    ret["precision"] = t.testPrecision()
    json_data = json.dumps(ret)
    return json_data

@app.route('/recall_test', methods=['GET'])
def recall_app():
    # returns the recall
    qTest=Query("stopwords.dat", "precision_recall_test_corpus.csv", "testIndex.pickle")
    qTest.storeStopwords()
    qTest.loadIndexFromFile()
    t = Test("testQueries.csv", qTest)
    # wrap the answer in json format
    ret = {}
    ret["recall"] = t.testRecall()
    json_data = json.dumps(ret)
    return json_data

if __name__ == "__main__":
	app.run(host="localhost", port=7000, debug=True)