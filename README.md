# Book-index
Given a (long) text, such as a book text, we want to produce a back-of-the-book index for it, i.e., provide a list of words that readers might search for in the text.
In fact I want to deal specifically with scientific texts (initially written in .tex (latex)), but except for a proper preprocessing, currently it doesn't make a difference.

Preprocessing and NLP concepts used:
- Preprocessing - erasing comments and formulas (mainly using regex).
- Named Entity Recognizer (NER) (an existing one, from spacy).
- Removing stop-words (using nltk list of such words).

Special dependencies: re (regex), nltk, spacy.

Further plans: 
- Part-of-speech (POS) tagging (from spacy): combine it - e.g. we'd only want nouns and adjectives.
- Do tf-idf for a given (math) text, comparing to some (large) collection of other math texts, in order to find the word significant in the given text. (Will try to get a collection from arXiv, and probably use only the abstracts as 'documents', due to time-space considerations :) ).
- Compare the produced list of words to an existing list (of 1-2 math books) to see how close it is to the human(expert)-produced list.
