 # -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import ast

def get_tf_idf_query_similarity(vectorizer,docs_tfidf,query):
	query_tfidf = vectorizer.transform([query])
	cosineSimilarities = cosine_similarity(query_tfidf, docs_tfidf).flatten()
	return cosineSimilarities
 
input_file="retrieval/다음뉴스_20220501_20220509_토큰화.csv"
df = pd.read_csv(input_file, header = 0)
documents=[]
remove=[]
#print('len df bef chk:',len(df))
for i,val in enumerate(df['토큰'].values):
	tokens=ast.literal_eval(val)
	if not tokens:
		remove.append(i)
		continue
	documents.append(" ".join(tokens))
df=df.drop(index=remove)
#print('len df aft chk:',len(df))
#print('len docs:',len(documents))

#vectorizer = TfidfVectorizer(preprocessor=nlp.clean_tf_idf_text)
vectorizer = TfidfVectorizer()
docs_tfidf = vectorizer.fit_transform(documents)

#input query by console input, input 끝	to terminate
import sys
read=sys.stdin.readline

def retrieval(query,rank=5):
	print('ready...')
	query=query.rstrip()

	cos_sim=get_tf_idf_query_similarity(vectorizer,docs_tfidf,query)
	cos_sim_item=sorted([(sim,i) for i,sim in enumerate(cos_sim)],reverse=True)
	
	ranked=[]
	for sim,i in cos_sim_item[:rank]:
		#print(sim)
		ranked.append(df.iloc[i,2])
        
	return ranked


#eval:mAP
