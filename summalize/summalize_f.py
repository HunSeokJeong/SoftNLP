
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
import math
#상대경로 입력
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from crawling import tokenizing
import pandas as pd


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


# news=["훔친 차를 몰다 사고를 낸 고교생이 의식을 잃은 동승자를 방치한 채 도망쳤다가 경찰에 붙잡혔다. 1일 경기 파주경찰서는 절도와 도로교통법 위반 등 혐의로 고교생 A군을 붙잡아 조사 중이라고 밝혔다. A군은 이날 오전 2시쯤 고양시 덕양구 화중로에 주차돼있던 SM5 승용차를 훔친 혐의를 받고 있다. A군은 차 안에 키가 있는 것을 찾아 고교생 B양을 태운 뒤 2시간 정도 고양 시내를 운전한 것으로 조사됐다. 그러다 A군은 오전 4시 25분쯤 파주시 조리읍 통일로변 한 주유소 앞을 지나다 주유소 출구 쪽 방호벽과 전신주를 들이받는 사고를 냈다. 이 사고로 조수석에 타고 있던 B양이 머리를 크게 다쳐 의식을 잃었으나 A군은 구호조치를 취하지 않고 B양을 인근 모텔 주차장에 옮긴 뒤 인근 야산으로 도망쳤다. 모텔 투숙객들은 사고 소리를 듣고 경찰에 신고했고 일부 투숙객들ㅇ느 모텔 주차장에 있던 B양을 발견해 병원에 이송됐다. 경찰은 오전 5시 50분쯤 야산에 숨어 있다 택시를 타고 도망치려던 A군을 체포했다. 장영락","법원 절도 범죄로 수 차례 처벌을 받고도 가석방된 지 9개월 만에 택시기사들을 상대로 돈을 훔친 20대가 실형을 선고받았다. 춘천지법 형사3단독 차영욱 판사는 상습야간주거침입절도와 사기 혐의로 기소된 A씨에게 징역 1년 6개월을 선고했다고 1일 밝혔다. A씨는 지난해 11월 초 춘천의 한 택시 조수석에 탄 후 입고있던 패딩 점퍼를 벗어 조수석 앞과 미터기를 가리고, 현금 7만5000원을 꺼내 훔친 혐의로 재판에 넘겨졌다. A씨가 지난 1월까지 총 20차례에 걸쳐 훔친 금액만 623만원에 달한다. 또 A씨는 지난해 12월 7일 새벽 춘천에서 정상적으로 요금을 지급하겠다며 화천을 경유해 춘천으로 돌아왔으나 요금 16만6000원을 지급하지 않았다. 지난 2020년 상습야간건조물침입절도죄로 징역 10개월을 선고받은 A씨는 지난해 2월 가석방된 이후 9개월 만에 또다시 범행을 저질렀다. 미성년자였던 시기에는 절도관련 범죄를 벌여 수 차례 소년보호사건으로 송치처분을 받았다. 차 판사는 일부 피해자의 회복을 제외하고는 피해자들이 입은 피해가 회복되지 않았다라며 피고인은 야간건조물침입절도죄 등으로 징역형의 집행유예 등을 선고받았음에도 누범기간에 또다시 이 사건 범행에 이른 점 등을 고려해 엄벌이 불가피하다고 설명했다.","614억원의 회삿돈을 횡령한 혐의로 구속영장이 청구된 우리은행 직원 A씨와 동생이 영장실질심사를 받기 위해 서울 서초구 서울중앙지법으로 들어가고 있다. 뉴시스 우리은행 회삿돈을 빼돌린 혐의를 받는 직원의 동생도 공범으로 함께 구속됐다. 서울중앙지법 허정인 판사는 1일 우리은행에서 거액을 빼돌린 A씨의 동생 B씨의 구속 전 피의자 심문을 진행한 뒤 증거인멸과 도주 우려가 있다며 구속영장을 발부했다. B씨는 형인 우리은행 직원 A씨와 공모해 총 614억원의 돈을 빼돌린 혐의를 받는다. 경찰은 지난달 27일 자수한 A씨의 계좌 거래 내역을 파악하던 중 횡령금 일부가 동생의 사업 자금으로 흘러간 단서를 포착해 이튿날 동생도 긴급체포했다. B씨는 형으로부터 약 100억 원을 받아 뉴질랜드 골프장 리조트 사업을 추진하다 80억여 원의 손실을 본 것으로 전해졌다. 두 사람이 횡령한 돈 대부분은 옛 대우일렉트로닉스 매각에 참여했던 이란 가전업체 엔텍합에 우리은행이 돌려줘야 하는 계약보증금인 것으로 파악됐다. 그러나 B씨는 이날 영장실질심사 출석하면서 처음부터 형과 범행을 계획했느냐, 골프장 사업에 돈을 썼느냐는 취재진의 질문에 아니다라며 부인했다. 또 자금 출처를 알고 있었느냐는 질문에도 몰랐다고 했다."]
# sums=[generate_summary(i,2) for i in news]
# for i in range(3):
# 	print("\n본문: ",news[i][:200],"(중략)")
# 	print("\n요약: ", sums[i])