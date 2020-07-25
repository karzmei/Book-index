# analysing results
import numpy as np
from sklearn import metrics
import pandas as pd

# internal import:
import preprocess_txts as preproc

def precision_recall(actual_set, predicts, text):
	""" calculating precision and recall values using scikit-learn over a range of thresholds: 
	for different thresholds of probabilities that were computer for each predicted word.
	INPUT: actual_set = set of actual index tokens. predicts = dictionary of predictions of probability for *some* of the text tokens,
	text = (string) the initial text, a bit cleaned."""
	

	all_words = set(preproc.text2list(text))  #cleaning as usual and turning into a set
	
	words_GT = {token: (token in actual_set) for token in all_words}  # 1 if token appears in actual set, otherwise: 0.
	words_GT_S = pd.Series(words_GT)
	# extending the predictions dictionary to all of words text (by adding zeros for words that don't appear in predicts):
	words_prob = {token : (predicts[token] if token in predicts else 0) for token in all_words}
	words_prob_S = pd.Series(words_prob)

	# convert to dafa frame
	tokens_df = pd.DataFrame({'Actual Y/N': words_GT_S, "Predictions probabilities": words_prob_S})
	
	print(tokens_df.head(20))
	#precision, recall, thresholds = metrics.precision_recall_curve(y_true, ???)

	#return precision, recall, thresholds