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
    #print("query : ",query_token)
    query_tfidf = vectorizer.transform([" ".join(query_token)])
    cosineSimilarities = cosine_similarity(query_tfidf, docs_tfidf).flatten()
	#쿼리 벡터와 기사 벡터 사이 코사인 유사도
    return cosineSimilarities
 

##run.py에서 호출하는 검색 함수, 검색결과 상위 기사의 본문 반환
def retrieval(query,rank=5):
	#print('ready...')
	print(f'\n[Tabloid Discriminator] "{query}" 검색을 준비합니다...')
	query=query.rstrip()
	cos_sim=get_tf_idf_query_similarity(vectorizer,docs_tfidf,query)
	
	#cos_sim_item에 query와의 (similarity,index) 튜플값 리스트 들어가고 유사도에 대해 내림차순 sorting함.
	cos_sim_item=sorted([(sim,i) for i,sim in enumerate(cos_sim)],reverse=True)
	
	ranked=[]
	for sim,i in cos_sim_item[:rank*10]:
		ranked.append([df.iloc[i,1], df.iloc[i,2], i])#주소,본문,인덱스
		
	# 검색된 뉴스 중, 내용 유사한 뉴스들 제거
	remove = []
	for i in range(rank*10):
		if i in remove: continue
		idx_a = ranked[i][2]
		current_news = docs_tfidf[idx_a].toarray()
		
		for j in range(i+1, rank*10, 1):
			if j in remove: continue
			idx_b = ranked[j][2]
			next_news = docs_tfidf[idx_b].toarray()
			
			cos_sim = float(cosine_similarity(current_news, next_news))
			if cos_sim >= 0.85 and j not in remove:     
				remove.append(j)
	
	remove.sort()
	for _ in range(len(remove)):
		idx = remove.pop()
		ranked.pop(idx)
	
	# 상위 뉴스 유사도 출력
        for i in range(len(ranked)):
		sim = ranked[i][3]
		print(f'[Tabloid Discriminator] 쿼리-검색된 뉴스와의 유사도: {sim}')
	return ranked[:rank]
	
	#for sim,i in cos_sim_item[:rank]:
	#	print(sim)
	#	#리턴값 [기사 링크, 기사 대본]
	#	ranked.append([df.iloc[i,1],df.iloc[i,2]])
	#return ranked


input_file="retrieval/tokenedNews.csv"
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
df=df.drop(index=remove) #제거할 기사들을 df에서 드랍
#print('len df aft chk:',len(df))
#print('len docs:',len(documents))

vectorizer = TfidfVectorizer()
#문서의 tf-idf 벡터
docs_tfidf = vectorizer.fit_transform(documents)

#eval:mAP
