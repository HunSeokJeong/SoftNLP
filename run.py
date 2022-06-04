from retrieval import retrieval_f
from summalize import summalize_f

query="검찰청장 수사"
for newsFeed in retrieval_f.retrieval( query,5):
    print(newsFeed)
    summalize_f.generate_summary(newsFeed, 1)