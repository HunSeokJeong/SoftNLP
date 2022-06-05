from retrieval import retrieval
from summalize import summalize
for newsFeed in retrieval.retrieval(10):
	summalize.generate_summary(newsFeed, 1)