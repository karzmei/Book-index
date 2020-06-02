# Book-index
Given a (long) text, such as a book text, we want to produce a back-of-the-book index for it, i.e., provide a list of words that readers might search for in the text. This job, when done seriously, is usually done by (at least somewhat-) experts in the field of the book topic, who manually (or half-manually, as there's software that they use that suggest words) create a suitable list of words, sometimes thinking even of "What words might the reader search for" the will lead them to this paragraph I'm reading now?". So the question is, can this be replaced by a computer?
[ONGOING]

How do I plan to find the index? (V marks what's already implemented - although maybe not yet used..)
The current idea combines several basic NLP concepts. First we search for candidates in the book text and then rate them:
- (V) Find all nouns.
- Find pairs of adjective + noun (or maybe several adjectives + noun). That's for later! :)
- (V) Add all Named Entities (let's say they should be included in the index in any case).
- (V) Remove any stop-words from the candidates list obtained in the process above. Just in case.
- (V) Then we can "rate" all candidates using tf-idf, where the idf is with respect to some corpus of texts in the same area as out main text (book).
- Set up some threshold to take only candidates above this threshold (to be fixed manually for now).
- Analysis: check how good the obtained list of words matches the actual existing index (precision etc.).
- Post-analysis: See if the result could be improved - maybe by taking *not* the classical tf-idf, and by adding "adjective+noun" pairs.

The data to check the idea: (hopefully, "proof of concept")
I took an "open-text" book in the field of Machine Learning as the book. As the corpus, I took a collection of arXiv-ed articles in this area, found of Kaggle (https://www.kaggle.com/neelshah18/arxivdataset/data#), *but* i'm using only their titles+abstracts, which might not be good enough for the idf part.


Make use of:
- Preprocessing and cleaning - erasing comments and formulas (mainly using regex) (for the case the input is a .tex file - currently not used). Cleaning index data from the digits and some weird effects of its production (using regex).
- Named Entity Recognizer (NER) (using spacy).
- Removing stop-words (using nltk list of such words).
- Part-of-speech (POS) tagging (from spacy).

Package dependencies: re (regex), nltk (for stop-words), spacy (for POS, NER), json (for the corpus data).


Side remark: Back in the days, a person (with access to a library) would open a book, and used its index in order to find specific topics inside or check if the book contains what they looked for. This was the vintage "Find" function. In electronic books, things got easier (so much easier, that some writers forget to add an index when producing a hard-copy book). It can be nice to be able to "close the circle" and produce a back-of-the-book index using some NLP and "automated" extensive search in a corpus of the same field of knowledge as the book (in attempt of replacing some "expert" knowledge).
