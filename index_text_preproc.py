import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re, string #regular expressions manipulations (string manipulations), be strong :(

import timeit # to measure running time while testing
from timeit import Timer

import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords

def remove_comments(text):
	'''
	removes .tex(=latex) comments from the text (string), returning a string clean of comments
	Remark1: commebts in .tex are made by % which comments out everything after this sign that comes on the same line
	Remark2: BUT we don't want to delete real percentage signs, i.e. if there's \% in the text, we don't want to remove it.
	Remark3: NEEDS text with punctuation, i.e. should be done BEFORE you remove punctuation
	Remark4: possibly the author used more fancy way of commenting, in which case the comments will not be spotted like this :(.
	''' 
	clean = re.sub(r'(?<!\\)\%.*\n', '', text) # don't PANIC!
	# Here \%. means match character after the sign %, * means zero (empty comment) or more, \n is there to include it, because it's not included in the "." that means all characters (except \n)
	# The (?<!\\) part is saying "look one carachter behind" the %, and if there's a \ there, then don't include this in the match. In any case, the match catches on;y stuff stating at %, not before.
	return clean

def remove_formulas(text):
	'''
	given a text(string), removes all formulas and .tex(latex) technical stuff which gives no (or not much) textual info, such as stuff between $$ signs, see a full list below.
	returns a string after these removed
	Remark1: NEEDS text with punctuation, i.e. should be done BEFORE you remove punctuation
	Remark2: In index, it could be that we do want formulas/notations to appear, so then we'd want to keep the formulas. We ignore this component by applying this function
	Remark3: removes from it the math parts, i.e. parts that are:
			- enclosed by $$-s (both sides), $-s (both sides), \[ \], \( \),
			- enclosed by \begin{equation}, \end{equation}, \begin{equation*}, same for: align, align*, tikzpicture, center
	'''
	# setting up some constants : delimeters to be used when deleting formulas:
	DELIMsymb = {"$$":"$$", "$":"$", "\[":"\]", "\(":"\)"} # delimeters that are symbolic (ie not begin-end stuff)
					# REMARK: it's important that $$ comes before $, because $ could ruin the existing $$s partly.
	DELIMbe = {'align', 'align*', 'equation', 'equation*', 'tikzpicture', 'center'} # a set of delimeters that come as \begin{command} ... \end{command}, be = begin-end
	# TODO this is not a complete list of begin-end stuff, and theoretically it could be any command, so have to make it more general

	# the syntax for re.sub is: 
	# re.sub(pattern, repl, string, count=0, flags=0) (substituting all patterns in string by repl)
	# pattern = what to search for (match), repl = what to replace the pattern with, string = where to search, count = ??, flags = other remarks, like re.DOTALL.
	# ? makes the search non-greedy, eg it searches from $ to the first next $ instead of the last $ in the document.
	# . means all (except special stuff like \n, for which the re.DOTALL serves)
	# TODO r means:  + means: ? means:

	cleaned = text
	# removing the first kind of formulas: enclosed by symbolic delimiters
	for opening, closing in DELIMsymb.items():
		pattern = re.escape(opening) + r'.+?' + re.escape(closing)
		cleaned = re.sub(pattern, '', cleaned, 0, re.DOTALL)		
		# eg: cleaned = re.sub(r'\$.+?\$', '', cleaned, 0, re.DOTALL)

	# removing the second kind of formulas: enclosed by begin{command} and end{command}
	for key in DELIMbe:
		cleaned = re.sub(r'\\begin{' + re.escape(key) + r'}.+?\\end{' + re.escape(key) + r'}', '', cleaned, 0, re.DOTALL)
		# eg: cleaned = re.sub(r'\\begin{align}.+?\\end{align}', '', cleaned, 0, re.DOTALL)
	# MISC
	# removing tex commands of the form \[command]{parameter}, e.g. \begin{definition} but leaving the text that might come after it, as inside a definition
	cleaned = re.sub(r'\\.+?}', '', cleaned, 0, re.DOTALL)
	# removing tex commands of the form \[command], e.g. \item 
	cleaned = re.sub(r'\\.+? ', '', cleaned, 0, re.DOTALL)

	return cleaned

def remove_punct(text):
	'''
	removes all punctuation from a text (string) and returns the "cleaned" text
	WARNING: not adviced to do remove_formulas or remove_comments after removing punctuation
	'''
	regex = re.compile('[%s]' % re.escape(string.punctuation))
	# first replacing punctuation signs with a space, to prevent words from sticking together (eg if the text doesn't spacing: "to be or not to be-that is the question")
	clean = regex.sub(' ', text)
	# then get rid of extra spaces:(not including \n (newline) or \t (tab) or \s (space) manually generated, but including such     spaces.)
	clean = re.sub(' +', ' ', clean)
	# this can be also done using text.strip()
	return clean


#######################################################################################################################################################
# TESTING #
if __name__ == "__main__": #the following lines won't be executed when this file is imported by some other "main" file

	text_file = open("rigid_flex.txt")
	mytext = text_file.read()
	text_file.seek(0) #back to beginning before going over it

	t = Timer(lambda: remove_formulas(mytext))
	print(t.timeit(number=1))