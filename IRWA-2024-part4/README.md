# IRWA Search Engine Project

## Description
This project aims to create a search engine based on a given query and display the top N results using a ranking algorithm adapted from a previous lab. Additionally, it provides statistics related to queries and user sessions.

## Project Structure
1. **search_engine**: Contains scripts for loading and processing the data corpus.
2. **web_app.py**: The main Flask application file that manages the web interface and interaction with the search engine.
3. **analytics_data.py**: Handles statistics related to queries and sessions.
4. **templates**: Contains HTML pages for displaying search results, tweet details, and statistics.

## Features
- **Search Engine**: Performs searches in the loaded corpus and displays ranked results.
- **Statistics**:
  - Click count per tweet.
  - Detailed query information.
  - Session data (ID, browser, operating system, IP, country, etc.).
- **Dashboard**: Displays visual statistics, including graphs for tweet click counts and tables for query and session data.

## Requirements
- Python 3.x
- Flask

## Running the Application
python web_app.py

