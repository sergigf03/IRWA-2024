
# Tweet Analysis and Information Retrieval System

## Overview
This notebook processes tweet data to create an information retrieval system. It focuses on preprocessing, indexing tweets, computing TF-IDF, and visualizing data with T-SNE.

## Features
- **Preprocessing**: Cleans and prepares tweet data.
- **Inverted Index**: Builds an inverted index for efficient searching.
- **TF-IDF Scoring**: Ranks tweets based on their relevance to queries.
- **Visualization**: Uses T-SNE to plot tweet embeddings.

## Setup
Install necessary libraries using:
```bash
pip install nltk numpy pandas matplotlib scikit-learn
```
Make sure to download NLTK stopwords with:
```python
nltk.download('stopwords')
```

## Usage
1. Mount your Google Drive
2. Run each cell to see the system build and process queries step-by-step. Modify paths and queries as needed for your dataset and objectives.
