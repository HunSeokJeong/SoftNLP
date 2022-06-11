from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from retrieval import retrieval_f
from summalize import summalize_f
from crawling import evaluation
from crawling import tokenizing
import pandas as pd


def evaluate(query):
	
	print("retrieval,summarize start")
	
	
	vectorizer = TfidfVectorizer()
	n=5
	documents=[]
	retrieval_news=retrieval_f.retrieval(query,n)
	for addr,content,idx in retrieval_news:
	    #print('_________________')
	    #print(content)
	    summalize_f.generate_summary(content, 1)
	    content_token=tokenizing.Tokenizer().get_clean_token(tokenizing.Tokenizer().refine_text(content))
	    documents.append(' '.join(content_token))
	
	docs_tfidf = vectorizer.fit_transform(documents)
	
	print('\n\n\n\n')
	
	
	print("crawling for eval start")
	searcher=evaluation.Searcher(query,10)
	answer=[False]*n
	for title,link,content in zip(searcher.searched_title,searcher.searched_link,searcher.searched_content):
	    content_token=tokenizing.Tokenizer().get_clean_token(tokenizing.Tokenizer().refine_text(content))
	    #print(title,link)
	    #print(content)
	    content_join=' '.join(content_token)
	    sim=retrieval_f.get_tf_idf_query_similarity(vectorizer,docs_tfidf,content_join)
	    print(sim)
	    for i in range(n):
	        if sim[i]>0.25:
	            answer[i]=True
	
	print(query)
	print(f'answer: {answer}')
	#mAP
	avg=0
	acc=0
	for i in range(1,n+1):
	    if answer[i-1]:
	        acc+=1
	        avg+=acc/i
	print(f'mAP: {avg/n}')
	
	return retrieval_news,zip(searcher.searched_title,searcher.searched_link,searcher.searched_content),answer,avg/n # 기존뉴스(주소,본문,인덱스),search뉴스(제목,링크,내용)
