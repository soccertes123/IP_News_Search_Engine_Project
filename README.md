# Toogle

First run the create index program:
python createIndex_tfidf.py stopWords.dat testCollection.dat testIndex.dat titleIndex.dat

Then run the query index program:
python svm.py stopWords.dat testIndex.dat
