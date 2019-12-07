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

# some constants
wantedNE = ("ORG","PERSON")
tresh = 0.2


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
	sw = stopwords.words('english') # nltk list of stopwords
	for token in w_list:
		if token in sw:
			w_list.remove(token)
	return w_list
# TODO: think how to use it and adjust accordingly

def named_ent(text):
	'''
	finds wanted named entities in a text, returning them as a set
	'''
	nlp = spacy.load("en_core_web_sm", disable=["tagger", "parser"]) #  want NER only
	doc = nlp(text)
	NE = set()
	for ent in doc.ents:
		if ent.label_ in wantedNE: # wanted Named Entities
			NE.add(ent.text)
	return NE
	# BUG: Alice and Alice\n are considered different. Why Alice\n even appears ???! #


######################################################################################################################################

if __name__ == "__main__": #the following lines won't be executed when this file is imported by some other "main" file
	text_file = open("aliceshort.txt")
	mytext = text_file.read()
	text_file.seek(0) #back to beginning before going over it

	mytext = clean_text(mytext)
	print(mytext)

	print(named_ent(mytext))

	tf = term_freq(mytext) # a dictionary of words and their tf

	tf_sorted = sorted(tf.items(), key = lambda kv: kv[1], reverse = True) # sorting tf by frequency in descending order (output is a list of pairs (word, tf))

	max_tf = tf_sorted[0][1] # first element value
	min_tf = tf_sorted[-1][1] # last element value
	tf_useful = [(token, val) for (token,val) in tf_sorted if (min_tf*(1+tresh) <= val <= max_tf*(1-tresh))] # relevant part of the list

