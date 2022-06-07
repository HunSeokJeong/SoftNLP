 # -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import ast

#상대경로 입력
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from crawling import tokenizing


##유사도를 값으로 가지는 일차원 <class 'numpy.ndarray'> (48527,) 반환
def get_tf_idf_query_similarity(vectorizer,docs_tfidf,query):
	#쿼리 tf-idf vector
    #토큰화+용언분석 적용 //파일경로 문제 있음.
    query_token=tokenizing.Tokenizer().get_clean_token(tokenizing.Tokenizer().refine_text(query))
    print("query : ",query_token)
    query_tfidf = vectorizer.transform([" ".join(query_token)])
    cosineSimilarities = cosine_similarity(query_tfidf, docs_tfidf).flatten()
	#쿼리 벡터와 기사 벡터 사이 코사인 유사도
    return cosineSimilarities
 

##run.py에서 호출하는 검색 함수, 검색결과 상위 기사의 본문 반환
def retrieval(query,rank=5):
	print('ready...')
	query=query.rstrip()
	cos_sim=get_tf_idf_query_similarity(vectorizer,docs_tfidf,query)
	
	#cos_sim_item에 query와의 (similarity,index) 튜플값 리스트 들어가고 유사도에 대해 내림차순 sorting함.
	cos_sim_item=sorted([(sim,i) for i,sim in enumerate(cos_sim)],reverse=True)
	
	ranked=[]
	for sim,i in cos_sim_item[:rank]:
		print(sim)
		#리턴값 [기사 링크, 기사 대본]
		ranked.append([df.iloc[i,1],df.iloc[i,2]])
	return ranked


input_file="다음뉴스_20220501_20220509_토큰화.csv"
df = pd.read_csv(input_file, header = 0)

##토큰이 없는 기사 (아마도 불용어 제거시 모두 제거되거나 본문자체가 없는 기사인듯..?) 제거	
documents=[]	#벡터화할 기사 (토큰들을 띄워쓰기 기준으로 합친 문자열 하나)를 값으로 가지는 일차원 배열
remove=[]	#제거할 기사 번호 임시로 담아둠

#print('len df bef chk:',len(df))
for i,val in enumerate(df['토큰'].values):
	tokens=ast.literal_eval(val)
	if not tokens:
		remove.append(i)
		continue
	documents.append(" ".join(tokens))
df=df.drop(index=remove) #제거할 기사들을 df에서 드랍
#print('len df aft chk:',len(df))
#print('len docs:',len(documents))

vectorizer = TfidfVectorizer()
#문서의 tf-idf 벡터
docs_tfidf = vectorizer.fit_transform(documents)

#eval:mAP