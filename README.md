# Toogle

First run the create index program:
python createIndex.py

Then run the query index program:
python query.py

We store an inverted index in a python dictionary, which holds information about the corpus in terms of words, documents, and word positioning.  Our query algorithm uses the index to match queries with documents.

Things to do:

Nick: look into Naive Bayes and see if we can switch the current query algorithm with a Naive Bayes classifier.

Tyler: create an ngrams program


Other things to do:
implement a ranking system upon document retrieval
precision/recall
