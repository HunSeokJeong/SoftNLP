 # -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import ast
#input query by console input, input 끝	to terminate
import sys
read=sys.stdin.readline

##유사도를 값으로 가지는 일차원 <class 'numpy.ndarray'> (48527,) 반환
def get_tf_idf_query_similarity(vectorizer,docs_tfidf,query):
	#쿼리 tf-idf vector
	#현재 토큰화 안돼있음, 아마 훈석님이 작성한 retrieval_f를 최종적으로 사용하게 될 것 같은데 거기에는 되어있어서 굳이 안함.
	query_tfidf = vectorizer.transform([query])
	#쿼리 벡터와 기사 벡터 사이 코사인 유사도
	cosineSimilarities = cosine_similarity(query_tfidf, docs_tfidf).flatten()
	return cosineSimilarities

##run.py에서 호출하는 검색 함수, 검색결과 상위 기사의 본문 반환
def retrieval(rank=5):
	#쿼리 입력	
	print('ready...')
	query=read().rstrip()

	#유사도 기준 정렬해서 (유사도, 기사번호)를 값으로 가지는 리스트
	cos_sim=get_tf_idf_query_similarity(vectorizer,docs_tfidf,query)
	cos_sim_item=sorted([(sim,i) for i,sim in enumerate(cos_sim)],reverse=True)
	
	#입력으로 받은 개수에 맞는 상위 요소의 본문 반환, 제목과 링크 출력
	ranked=[]
	for sim,i in cos_sim_item[:rank]:
		print(df.iloc[i,0])	#제목
		print(df.iloc[i,1])	#링크	
		ranked.append(df.iloc[i,2])	#본문
	return ranked


input_file="retrieval/다음뉴스_20220501_20220523_토큰화.csv"
df = pd.read_csv(input_file, header = 0)

##토큰이 없는 기사 (아마도 불용어 제거시 모두 제거되거나 본문자체가 없는 기사인듯..?) 제거	
documents=[]	#벡터화할 기사 (토큰들을 띄워쓰기 기준으로 합친 문자열 하나)를 값으로 가지는 일차원 배열
remove=[]	#제거할 기사 번호 임시로 담아둠

#print('len df bef chk:',len(df))
for i,val in enumerate(df['본문토큰'].values):
	tokens=ast.literal_eval(val)
	if not tokens:
		remove.append(i)
		continue
	documents.append(" ".join(tokens))
df=df.drop(index=remove)	#제거할 기사들을 df에서 드랍
#print('len df aft chk:',len(df))
#print('len docs:',len(documents))


vectorizer = TfidfVectorizer()
#문서의 tf-idf 벡터
docs_tfidf = vectorizer.fit_transform(documents)

