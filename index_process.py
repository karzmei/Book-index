import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re, string #regular expressions manipulations (string manipulations)

from collections import defaultdict

import timeit # to measure running time while testing
from timeit import Timer

from nltk.corpus import stopwords

import spacy

# inner import
import index_text_preproc as preproc

# some COSTANTS
wantedNE = ("ORG","PERSON", "NORP") # relevant Named Entities types
wantedPOS = ("NOUN", "PROPN", "ADJ") # relevant Part-Of-Speech types
tresh = 0.2
#####################################################################################################

def clean_text(text):
	'''
	Removing (tex) comments, removing formulas
	'''
	clean = preproc.remove_comments(text)
	clean = preproc.remove_formulas(clean)
	return clean

def words_count(words_list):
	'''
	Counts how many times each word appears in the list, returning a dictionary with elements (word, #times it appears)
	'''
	words_list = [word.lower() for word in words_list] #all to lowercase

	words_stat = {}
	for word in words_list:
		if word in words_stat: # if the word is already in the dictionary, increase its count by 1
			words_stat[word] += 1
		else: # if it's the first appearance, add it
			words_stat[word] = 1
	return words_stat

def term_freq(text):
	''' For each word in the text, computes its term frequency (tf), ie, 
		the number of times it appears in the text, divided by the total number of words in the text
		stores it in a dictionary of (word, tf)
	'''
	text = preproc.remove_punct(text)
	words_list = text.split()
	words_amount = len(words_list)
	words_tf = words_count(words_list) #initializing with the counting of how many times each word appears, obtaining a dictionary: (word, #times)
	total = float(sum(words_tf.values()))
	words_tf = {k: v / total for k, v in words_tf.items()}

	return words_tf

def remove_stopwords_list(w_list):
	'''
	Removing (english) stop words from a list a words (w_list), returning a "cleaned" list
	'''
	sw = stopwords.words('english') # nltk list of stopwords (spacy also has one, but i prefer nltk for now)
	cleaned = [token for token in w_list if (token not in sw)]
	return cleaned

def named_ent(text):
	'''
	finds wanted named entities in a text, returning them as a set
	'''
	nlp = spacy.load("en_core_web_sm", disable=["tagger", "parser"]) #  want NER only
	doc = nlp(text)
	NE = set()
	for ent in doc.ents:
		if ent.label_ in wantedNE: # wanted Named Entities
			# BUG: Spacy tokenizer does not separate \n, I get "Alice\n" and alike. So need to delete manually, till it's resolved:
			NE.add(ent.text.replace('\n', ''))
#	NE = (ent.text for ent in doc.ents if ent.lable_ in wantedNE) # shorter
	return NE


def pos_greedy(text):
	'''
	Removes from w_list tokens that are not in the wanted list of Part-of-Speech types. 
	Greedy: enough for a token to be once in the wanted list to stay in the list.
	We assume that w_list contains words from the text only, although the function will run anyway
	(the assumption is because w_list might not be all words, but part of them, after some preprocessing, eg erasing stopwords)
	'''
	nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"]) #  use the pos tagging here
	doc = nlp(text)
	candidates = set()
	for token in doc:
		if token.pos_ in wantedPOS:
			candidates.add(token.text)
	return candidates

######################################################################################################################################

if __name__ == "__main__": #the following lines won't be executed when this file is imported by some other "main" file
	text_file = open("aliceshort.txt")
	mytext = text_file.read()
	text_file.seek(0) #back to beginning before going over it

	mytext = clean_text(mytext)
	print(mytext)

	print(named_ent(mytext))

	tf = term_freq(mytext) # a dictionary of words and their tf
	non_stop_list = remove_stopwords_list(tf.keys()) # removing stop-words:
	print(non_stop_list)

	tf_sorted = sorted(tf.items(), key = lambda kv: kv[1], reverse = True) # sorting tf by frequency in descending order (output is a list of pairs (word, tf))

	print(pos_greedy(mytext))