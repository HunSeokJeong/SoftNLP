<<<<<<< HEAD
from retrieval import retrieval
from summalize import summalize
for newsFeed in retrieval.retrieval(10):
	summalize.generate_summary(newsFeed, 1)
=======
from retrieval import retrieval_f
from summalize import summalize_f

query="검찰청장 수사"
for newsFeed in retrieval_f.retrieval( query,5):
    print(newsFeed)
    summalize_f.generate_summary(newsFeed, 1)
>>>>>>> b469bc9cf2c204b14a739f74762f91a5d4f0fb10
