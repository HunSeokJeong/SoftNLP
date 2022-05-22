import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import ast

def get_tf_idf_query_similarity(vectorizer,docs_tfidf,query):
	query_tfidf = vectorizer.transform([query])
	cosineSimilarities = cosine_similarity(query_tfidf, docs_tfidf).flatten()
	return cosineSimilarities


input_file="다음뉴스_20220501_20220509_토큰화.csv"
df = pd.read_csv(input_file, header = 0)
documents=[]
for val in df['토큰'].values:
	tokens=ast.literal_eval(val)
	if not tokens:
		continue
	documents.append(" ".join(tokens))
#documents=np.array(documents,dtype=object)
#documents=documents.astype('U')

#vectorizer = TfidfVectorizer(preprocessor=nlp.clean_tf_idf_text)
vectorizer = TfidfVectorizer()
docs_tfidf = vectorizer.fit_transform(documents)

#input query by console input, input 끝	to terminate
import sys
read=sys.stdin.readline
print('ready...')
while True:
	query=read().rstrip()
	if query=='끝':
		break
	cos_sim=get_tf_idf_query_similarity(vectorizer,docs_tfidf,query)
	cos_sim_item=sorted([(sim,i) for i,sim in enumerate(cos_sim)],reverse=True)
	
	for sim,i in cos_sim_item[:5]:
		print(df.iloc[i,1], sim)



#eval:mAP
