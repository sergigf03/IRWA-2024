from lab3_u199880_u198725 import *

def search_in_corpus(query,total_docs, corpus, top_n=10):
    # 1. Create TF-IDF index using the inverted index method from your previous code
    inverted_index = create_inverted_index(corpus)

    # 2. Preprocess the query and get the query terms
    query_processed = build_terms(query)

    # 3. Rank the documents based on cosine similarity of TF-IDF vectors
    ranked_docs = rank_documents_tf_idf_cosine(inverted_index, query_processed, total_docs)

    return ranked_docs[:top_n]
