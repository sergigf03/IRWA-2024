import random

from myapp.search.objects import ResultItem, Document
from myapp.search.algorithms import *


def build_demo_results(corpus: dict, search_id):
    """
    Helper method, just to demo the app
    :return: a list of demo docs sorted by ranking
    """
    res = []
    size = len(corpus)
    ll = list(corpus.values())
    for index in range(random.randint(0, 40)):
        item: Document = ll[random.randint(0, size)]
        res.append(ResultItem(item.id, item.title, item.description, item.doc_date,
                              "doc_details?id={}&search_id={}&param2=2".format(item.id, search_id), random.random()))

    # for index, item in enumerate(corpus['Id']):
    #     # DF columns: 'Id' 'Tweet' 'Username' 'Date' 'Hashtags' 'Likes' 'Retweets' 'Url' 'Language'
    #     res.append(DocumentInfo(item.Id, item.Tweet, item.Tweet, item.Date,
    #                             "doc_details?id={}&search_id={}&param2=2".format(item.Id, search_id), random.random()))

    # simulate sort by ranking
    res.sort(key=lambda doc: doc.ranking, reverse=True)
    return res


class SearchEngine:
    """Educational search engine"""

    def search(self, search_query, search_id, corpus):
        print("Search query:", search_query)

        results = []
        total_docs = len(corpus)

        # Get the search results based on the query
        ranked_docs = search_in_corpus(search_query, total_docs, corpus)

        # Format the results as instances of ResultItem
        for doc_id, ranking in ranked_docs:
            # Assuming `corpus` is a list of Document objects, retrieve the document
            document = corpus.get(doc_id)  # Get the actual document object using the doc_id
            
            # Create a ResultItem for each ranked document
            result_item = ResultItem(
                id=document.id,
                title=document.title,
                description=document.description,
                doc_date=document.doc_date,
                url=document.url,
                ranking=ranking
            )
            
            # Append the result item to the list
            results.append(result_item)

        return results
