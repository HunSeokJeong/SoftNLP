
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
import math
#상대경로 입력
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from crawling import tokenizing

def get_token(text):
    return tokenizing.Tokenizer().get_clean_token(tokenizing.Tokenizer().refine_text(text))

def read_article(filedata):
    filedata=filedata.replace("?",".")
    article = filedata.split(". ")
    sentences = []
    for sentence in article:
        #print(sentence)
        token=get_token(sentence)
        if len(token)>0:
            sentences.append([sentence,get_token(sentence)])


    return sentences

#유사도 구하는 부분
def sentence_similarity(sent1, sent2):

    all_words = list(set(sent1 + sent2))
 
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)
 
    # build the vector for the first sentence
    for w in sent1:
        vector1[all_words.index(w)] += 1
 
    # build the vector for the second sentence
    for w in sent2:
        vector2[all_words.index(w)] += 1
 
    return 1 - cosine_distance(vector1, vector2)
 
def build_similarity_matrix(sentences):
    # Create an empty similarity matrix
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
 
    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2: #ignore if both are same sentences
                continue 
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2])

    return similarity_matrix


def generate_summary(file_name, top_n=5):
    
    summarize_text = []

    # Step 1 - Read text anc split it
    sentences =  read_article(file_name)

    # Step 2 - Generate Similary Martix across sentences
    sentence_similarity_martix = build_similarity_matrix([i[1] for i in sentences])
    # print(sentence_similarity_martix)

    # Step 3 - Rank sentences in similarity martix
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
    
    scores = nx.pagerank(sentence_similarity_graph)

    # Step 4 - Sort the rank and pick top sentences
    ranked_sentence = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)
    size=len(ranked_sentence)
    if size<=top_n:
        top_n=size
    for i in range(top_n):
      summarize_text.append(ranked_sentence[i][1][0])

    # Step 5 - Offcourse, output the summarize texr
    return ". ".join(summarize_text)

# let's begin
