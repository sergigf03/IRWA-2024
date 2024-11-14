# Tweet Document Retrieval System

## Overview
This project is a tweet retrieval system that ranks tweets by relevance to specific queries using various scoring methods: TF-IDF + Cosine Similarity, BM25 + Cosine Similarity, Word2Vec + Cosine Similarity, and an Engagement-based Score (P-Score).

## Requirements
To run this notebook, you need to have the following installed:

- Python 3.x
- Jupyter Notebook or Jupyter Lab (or just use Google Collab)
- The following Python libraries:
  - Pandas
  - NumPy
  - Matplotlib
  - Any additional libraries used in the notebook

# Data Files:
  1. farmers-protest-tweets.json: Dataset of tweets.
  2. tweet_document_ids_map.csv: Maps tweet IDs to document IDs.
# Steps
  1. Data Loading & Preprocessing:
        - Load and preprocess tweet content (remove stopwords, punctuation, and apply stemming).
        - Extract hashtags, likes, retweets for engagement metrics.
  2. Inverted Index Creation
        - Build an inverted index mapping terms to document positions for efficient retrieval.
  3. Scoring Methods
        - TF-IDF + Cosine Similarity: Scores based on term frequency and rarity across documents.
        - BM25 + Cosine Similarity: Enhances TF-IDF with document length normalization.
        - Word2Vec + Cosine Similarity: Uses word embeddings to capture semantic relevance.
        - Engagement-Based Score: Ranks tweets by social engagement (likes, retweets).
