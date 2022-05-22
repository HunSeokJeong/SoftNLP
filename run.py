from retrieval import retrieval
from summalize import summalize
for newsFeed in retrieval.retrieval(5):
	summalize.generate_summary(newsFeed, 1)