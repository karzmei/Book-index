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
	print("in totol, there are %d distinct word in the text, after cleaning", len(all_words))
	
	words_GT = {token: (1 if token in actual_set else 0) for token in all_words}  # 1 if token appears in actual set, otherwise: 0.
	words_GT_S = pd.Series(words_GT)
	print("there are %d words in the GT index", len(words_GT), )
	assert(len(words_GT == words_GT_S.size()))


	# extending the predictions dictionary to all of words text (by adding zeros for words that don't appear in predicts):
	words_prob = {token : (predicts[token] if token in predicts else 0) for token in all_words}
	words_prob_S = pd.Series(words_prob)
	print("in total, there are %d candidates for index", len(words_prob))

	# convert to dafa frame
	tokens_df = pd.DataFrame({'actual index': words_GT_S, 'predict_probs': words_prob_S})
	
	print(tokens_df.head(20))
	# GT values (of 1/0) for all tokens:
	y_true = (tokens_df.loc[:,'actual index']).values  # taking the actual index 1(Y)/0(N) values
	pred_probs = (tokens_df.loc[:,'predict_probs']).values

	#print("size of y_true is: ", size(y_ture))
	#print("size of pred_probs is: ", size(pred_probs))

	return metrics.precision_recall_curve(y_true, pred_probs)  # returns arrays of precision, recall, thresholds
