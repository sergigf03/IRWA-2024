from collections import defaultdict
from array import array
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import math
import numpy as np
from numpy import linalg as la


# if you do not have 'nltk', the following command should work "python -m pip install nltk"
import nltk
nltk.download('stopwords')

tweets_path = 'farmers-protest-tweets.json'
tweet_doc_ids_map_path = 'tweet_document_ids_map.csv'
evaluation_path = 'evaluation.csv'

import json
import re
import string
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


def build_terms(line):
    """
    Preprocess the tweet content by removing stop words, punctuation, and applying stemming.

    Argument:
    line -- string (text to preprocess)

    Returns:
    A list of tokens corresponding to the preprocessed text.
    """
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words("english"))

    # Convert to lowercase
    line = line.lower()

    # Remove punctuation (except for #)
    line = line.translate(str.maketrans('', '', string.punctuation.replace('#', '')))

    # Tokenize the text
    line = line.split()

    # Remove stopwords
    line = [word for word in line if word not in stop_words]

    # Apply stemming
    line = [stemmer.stem(word) for word in line]

    return line

# Function to extract hashtags from the tweet
def extract_hashtags(text):
    """
    Extracts hashtags from the tweet content.

    Argument:
    text -- string (tweet content)

    Returns:
    hashtags - a list of hashtags found in the tweet
    """
    hashtags = re.findall(r'#\w+', text)  # Find hashtags using regular expressions
    return hashtags

# Function to process a tweet and return the required structure
def process_tweet(tweet):
    """
    Processes a single tweet and returns the required information structure, including document ID.

    Argument:
    tweet -- dictionary containing tweet data

    Returns:
    processed_tweet -- dictionary with the tweet's preprocessed content and metadata
    """

    tweet_content = tweet['content']  # Get the tweet content

    # Preprocess the tweet content
    preprocessed_content = build_terms(tweet_content)

    # Extract hashtags
    hashtags = extract_hashtags(tweet_content)

    # Structure the final output
    processed_tweet = {
        'Tweet': ' '.join(preprocessed_content),  # Preprocessed tweet content
        'Date': tweet['date'],
        'Hashtags': hashtags,
        'Likes': tweet['likeCount'],
        'Retweets': tweet['retweetCount'],
        'Url': tweet['url']
    }

    return  processed_tweet

def create_inverted_index(tweets_data):
    """
    Creates an inverted index for the protest tweets dataset.

    Arguments:
    tweets_data -- list of tweet dictionaries with fields like 'id' and 'content'

    Returns:
    inverted_index -- dictionary with terms as keys and posting lists as values.
                      Each posting list contains tuples of (document ID, positions).
    """
    inverted_index = defaultdict(list)

    # Loop through each tweet
    for tweet in tweets_data:
        terms = build_terms(tweets_data[tweet].description) 

        # Create a dictionary to track term positions in the current tweet
        current_tweet_index = defaultdict(lambda: [tweet, []])  # [tweet_id, list of positions]

        # Loop through the terms and store their positions
        for position, term in enumerate(terms):
            current_tweet_index[term][1].append(position)

        # Merge the current tweet index with the main inverted index
        for term, posting in current_tweet_index.items():
            inverted_index[term].append(posting)

    return inverted_index


def compute_tf_idf(inverted_index, total_docs, term, doc_id):
    term_occurrences = [posting for posting in inverted_index[term] if posting[0] == doc_id]
    if not term_occurrences:
        return 0
    tf = len(term_occurrences[0][1])  # Número de veces que el término aparece en el documento
    df = len(inverted_index[term])  # Número de documentos que contienen el término
    idf = math.log(total_docs / (df + 1))  # Añadir 1 para evitar la división por cero
    tf_idf = tf * idf
    return tf_idf

def build_document_vectors(inverted_index, query_terms, total_docs):
    doc_vectors = defaultdict(lambda: np.zeros(len(query_terms)))  # Inicializa los vectores de documentos
    for i, term in enumerate(query_terms):
        if term in inverted_index:
            for doc_id, _ in inverted_index[term]:
                tf_idf_score = compute_tf_idf(inverted_index, total_docs, term, doc_id)
                doc_vectors[doc_id][i] = tf_idf_score
    return doc_vectors

def build_query_vector(inverted_index, query_terms, total_docs):
    query_vector = np.zeros(len(query_terms))
    for i, term in enumerate(query_terms):
        if term in inverted_index:
            df = len(inverted_index[term])  # Document frequency for the term
            idf = math.log(total_docs / (df + 1))
            query_vector[i] = idf
    return query_vector

def cosine_similarity(query_vector, doc_vector):
    dot_product = np.dot(query_vector, doc_vector)
    query_magnitude = np.linalg.norm(query_vector)
    doc_magnitude = np.linalg.norm(doc_vector)
    if query_magnitude == 0 or doc_magnitude == 0:
        return 0
    return dot_product / (query_magnitude * doc_magnitude)

def rank_documents_tf_idf_cosine(inverted_index, query_terms, total_docs):
    doc_vectors = build_document_vectors(inverted_index, query_terms, total_docs)
    query_vector = build_query_vector(inverted_index, query_terms, total_docs)

    doc_scores = {}
    for doc_id, doc_vector in doc_vectors.items():
        similarity = cosine_similarity(query_vector, doc_vector)
        doc_scores[doc_id] = similarity

    ranked_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
    return ranked_docs




