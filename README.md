# Book-index
Given a (long) text, such as a book text, we want to produce a back-of-the-book index for it, i.e., provide a list of words that readers might search for in the text.

Preprocessing and NLP concepts used:
- Preprocessing - erasing comments and formulas (mainly using regex).
- Named Entity Recognizer (NER) (using spacy).
- Removing stop-words (using nltk list of such words). Might be removed later, if it's redundent.
- Part-of-speech (POS) tagging (from spacy): combine it - e.g. we'd only want nouns and adjectives.

Package dependencies: re (regex), nltk, spacy.

Further plans: 
- capture adjective+noun pairs (of more than one adjective), probably using spacy's dependencies parser.
- Do tf-idf for a given text, comparing to some (large) collection of other texts in the same field, in order to find the word significant in the given text. For the "proof-of-concept", i'll use a book (that includes an index) in the field of ML and a collection of arXiv-ed articles in this area, found of Kaggle (https://www.kaggle.com/neelshah18/arxivdataset/data#).
- Compare the produced list of words to an existing list (of 1-2 math books) to see how close it is to the human(expert)-produced list.
