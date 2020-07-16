# obtain book index candidates, using baisc NLP notions

import numpy as np
import re
import spacy
import json


from nltk.corpus import stopwords

# internal import:
import preprocess_txts as preproc

wantedNE = ("ORG","PERSON", "NORP") # relevant Named Entities types
wantedPOS = ("NOUN", "PROPN")  #, "ADJ") # relevant Part-Of-Speech types
corpus_PATH = "data/corpus_arxiv.json"
corpus_st_PATH = "data/corpus_st.json"
# functions to write:
# (* LATER) : get pairs of adjective+noun


def get_named_ent(text, wanted_NE):
	'''
	Finds wanted named entities in a text, returning them as a set
	'''
	nlp = spacy.load("en_core_web_sm")  #  want NER only
	doc = nlp(text)
	NE = set()
	for ent in doc.ents:
		if ent.label_ in wanted_NE: # wanted Named Entities
			# "BUG": Spacy tokenizer does not separate \n, I get "Alice\n" and alike. So need to delete manually, till it's resolved:
			NE.add(ent.text.replace('\n', ''))
#	NE = {ent.text for ent in doc.ents if ent.lable_ in wanted_NE} # shorter but without the correction.
	return NE


def get_wanted_pos(text, wanted_POS):
	'''
	Returns a set of all text words that are of the wnated POS types (eg, NOUNs)
	'''
	nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"]) #  use the pos tagging here
	doc = nlp(text)
	return {token.text for token in doc if token.pos_ in wanted_POS}


def sort_dict2list(words_dict, descend = True):
	""" Input is a dictionary of (string, numerical value),
	Output: a list consisting of the same pairs, ordered by the values.
	By default, the order is descending."""
	sorted_lst = sorted(words_dict.items(), key=lambda x: x[1], reverse = descend)
	return sorted_lst


def remove_stopwords_list(w_list):
	'''
	Removing (english) stop words from a list a words (w_list), returning a "cleaned" list
	'''
	sw = stopwords.words('english') # nltk list of stopwords (spacy also has one, but i prefer nltk for now)
	cleaned = [token for token in w_list if (token not in sw)]
	return cleaned


def words_count_in_txt(text_words_list, wanted_words_set):
	'''
	Counts how many times each word from the wanted_words_set appears in the text_words_list,
	Returning a dictionary with elements (word, #times it appears)
	(text is string, words_list is a list of strings)
	NOTE: everything is in lower-case for now.
	Returning also the total number of 
	'''
	text_words_list = [token.lower() for token in text_words_list]
	if wanted_words_set == {}:
		wanted_words_set = set(text_words_list)
	wanted_words_set = {token.lower() for token in wanted_words_set} #all to lowercase
	
	words_stat = {token: 0 for token in wanted_words_set}
	for token in text_words_list:
		if token in wanted_words_set:  # only interested in counting those
			words_stat[token] += 1  
		# words_stat was predefined with all words from wanted_words_set, so no need to check it the word exists there and manually add if not
	return words_stat


def term_freq(text, words_set):
	''' For each word from words_set, computes its term frequency (tf) in the text, ie, 
		the number of times it appears in the text, divided by the total number of words in the text
		stores it in a dictionary of pairs (word, tf)
		If words_set is empty, counts for all words of the text
	'''
	text_words_list = preproc.text2list(text)
	total_words_num = len(text_words_list)
	words_tf = words_count_in_txt(text_words_list, words_set)
	words_tf = {k: v / total_words_num for k, v in words_tf.items()}

	return words_tf

def df_slow_wo_precalc(corpus, words_set):
	""" Computed the document frequency (df) of each word from words_set wrt corpus (list of strings).
	Document frequency of a token t is defined to be:
	the number of documents from corpus in which this word appears 
	(at least once, we don't case how many times per document).
	NOTE: this is a pre-calculation for inverse-documnet-frequency(idf).
	Returns a dictionary with pairs (word, its df).
	NOTE: all in lower-case. (ingnoring case)
	"""
	stats = {token.lower():0 for token in words_set}  # initializing a dictionary

	for doc in corpus:
		for token in stats.keys():
			match = re.search(re.escape(token.lower()), doc, re.IGNORECASE)
			if match:
				stats[token] += 1

	return stats


def df(corpus_stats, words_set):
	""" Computes the document frequency (df) of each word from words_set wrt corpus (list of strings), 
	based on pre-calculated document frequencies for all words of the corpus.
	Document frequency of a token t is defined to be:
	the number of documents from corpus in which this word appears 
	(at least once, we don't case how many times per document).
	NOTE: this is a pre-calculation for inverse-documnet-frequency(idf).
	Returns a dictionary with pairs (word, its df).
	NOTE: all in lower-case. (ingnoring case)
	NOTE: Uses pre-calculated frequencies in the corpus.
	"""
	stats = { token:0 for token in words_set }  # initializing as a dictionary

	for token in words_set:
		if token in corpus_stats:
			stats[token] = corpus_stats[token]
	return stats


def idf(corpus_stats, words_set, corpus_len):
	""" Computes the inverse documnet frequency per each word from words_set wrt the corpus (list of strings).
	It's defined by: log (N / df(word)+1), where
		df(word) = # documents from corpus in which the word appears,
		N = corpus_len = # of documents in corpus.
	Returns a dictionary with (word: idf(word))
	NOTE: All in lower-case. (ignoring case)
	NOTE: Based of a pre-calculated statistics of documents prefuencies for all words from the corpus.
	"""
	dfs = df(corpus_stats, words_set)
	return {token: np.log( corpus_len / ( dfs[token]+1 ) ) for token in dfs.keys()}


def tf_idf(corpus_stats, text, words_set, corpus_len):
	""" Returns tf(word) * idf (word) for each word from words_set, wrt the text and the corpus of documents.
	See detailed definitions inside idf and term_freq functions as well. The definition is:
	tf(token) wrt to text = # time it appears in text
	idf(token) = log ( N / (# docs from corpus the token appears in, +1) ), where N is the number of documents in corpus.
	NOTE: we ignore case (everything is in lower-case)
	"""

	tfs = term_freq(text, words_set)
	idfs = idf(corpus_stats, words_set, corpus_len)

	return {token: tfs[token] * idfs[token] for token in tfs.keys()}


def candidates_scores(text, corpus_source = corpus_PATH, corpus_stats_source = corpus_st_PATH):
	""" Return tokens (single words for now) that are potentially good to appear in the text's index, and their "score".
	For now, the score is just the tf-idf. Corpus statistics loaded from a pre-calculated json file."""
	# Create the candidates set: by POS only, for now.
	# TO ADD: NE; pairs of adj-noun.

	# candidates set based on POS only, for now.
	cand_set = get_wanted_pos(text, wantedPOS)
	cand_set = {token.lower() for token in cand_set}
	
	# load corpus statistics
	with open(corpus_stats_source, 'r') as corpus_st_file:
		corpus_stats = json.load(corpus_st_file)  # this is a dictionary {word, df}

	# load the corpus itself (a json file)
	with open(corpus_source, 'r') as jfile:
		jdata = jfile.read()
    # parse file
	corpus = json.loads(jdata)
	corpus_length = len(corpus)
	# And their rates: (as a dictionary)
	cand_dict = tf_idf(corpus_stats, text, cand_set, corpus_length)
	
	# return as a list sorted by scores:
	return sort_dict2list(cand_dict, True)
# return_index_candidates(book_text, corpus) : 
# the main function here that returns a dictionary of word-rate(tf-idf or some other rate)


def corpus_precounting(corpus):
	""" Creates a dictionary that contains all the words appearing in the corpus 
	(ie in the union of all documents in the corpus), counting for each word 
	in how many docs if appeared (documnet frequency)"""
	stats = {}
	for doc in corpus:
		doc_words_lst = preproc.text2list(doc.lower())
		doc_words_set = set(doc_words_lst)
		#doc_stats = [token:1 for token in doc_words_set]  # dictionary for current doc
		for token in doc_words_set:
			if token in stats:
				stats[token] += 1
			else:
				stats[token] = 1
	return stats


def calc_and_save_corpus_stats(corpus_jsource = corpus_PATH):
	""" Opens the json file with the corpus documnets, pre-calculates the statistics of document frequency for all words, 
	and saves this to a json file"""
	with open(corpus_jsource, 'r') as jfile:
		jdata = jfile.read()
    # parse file
	jobj = json.loads(jdata)
	corpus = preproc.extract_json_abstract(jobj)
	# pre-calculating statistics: documnet frequency for each word from the corpus:
	corpus_stats = corpus_precounting(corpus)
	#saving to json file:
	corpus_st_file = open(corpus_st_PATH, "w")
	json.dump(corpus_stats, corpus_st_file)
	corpus_st_file.close()
	return True
#####################################################################################################




if __name__ == '__main__':
 	
	book_file = open("data/book_no_index.txt")
	book_txt = book_file.read()

	# tf-idf
	print(candidates_scores(book_txt, corpus_PATH, corpus_st_PATH))
	
	#print(preproc.remove_non_ascii(book_txt))