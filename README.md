# Search engine project for independent study
<!-- 
Authors: Tyler Schon, Nick Murray
Date: May, 2019
-->

First run the create index program:
python createIndex.py

Then run the query index program:
python query.py

We store an inverted index in a python dictionary, which holds information about the corpus in terms of words, documents, and word positioning.  Our query algorithm uses the index to match queries with documents.

First, create an index by running "createIndex.py". Then, try querying the index by running "query.py" and typing in a query; note you can also check out our precision/recall through this file, but you first have to create a testPRIndex.pickle file with the createIndex program by changing the name of the corpus and pickle files within the "createIndex.py" file.  Create the ngrams table by running "create_ngram_table.py".  Then, run the ngrams program by running "ngrams.py" and typing in a query.  You can also run the API by running "__init__.py".

Things to do:
implement ui?
naive bayes?
