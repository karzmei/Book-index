# main: generating book index
import numpy as np
import json

# internal import:
import preprocess_txts as preproc
import nlp_operations as nlp_oper
import analysis as analysis

wantedNE = ("ORG","PERSON", "NORP") # relevant Named Entities types
wantedPOS = ("NOUN", "PROPN")  #, "ADJ") # relevant Part-Of-Speech types
corpus_PATH = "data/corpus_arxiv.json"
corpus_st_PATH = "data/corpus_st.json"


if __name__ == '__main__':
	# load book text	
	with open('data/book_no_index.txt', 'r', encoding='utf-8') as txtfile:
		book_txt = txtfile.read()

	# load book corpus (json format)
	with open("data/corpus_arxiv.json", 'r') as jfile:
		jdata = jfile.read()
    # parse json file
	jobj = json.loads(jdata)

	corpus = preproc.extract_json_abstract(jobj)
	# obtain index candidates(book_text, corpus)
	candidates = nlp_oper.candidates_scores(book_txt, corpus_PATH, corpus_st_PATH)
	# print(candidates)
	# load the index and clean it:
	index_file = open("data/book_index.txt")
	index = index_file.read()
	index_set = preproc.get_index_set(index)

	# analyze and choose threshold
	precision, recall, thresholds = analysis.precision_recall(index_set, candidates, book_txt)



