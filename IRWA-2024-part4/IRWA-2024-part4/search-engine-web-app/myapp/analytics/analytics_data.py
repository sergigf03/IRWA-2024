import json
import random
from collections import defaultdict

class AnalyticsData:
    """
    In-memory persistence object for tracking and analyzing website usage.
    """

    # statistics tables
    fact_clicks = defaultdict(int)  # Click counter per document
    fact_queries = defaultdict(dict)  # Query tracking
    fact_sessions = defaultdict(dict)  # Session data
    fact_dwell_times = defaultdict(list)  # Dwell times per document
    fact_document_rankings = defaultdict(list)  # Document rankings per query

    def __init__(self):
        # This would initialize any necessary fields for session or query tracking
        pass

    def save_click(self, doc_id: int):
        """
        Save a click event for a specific document.
        """
        self.fact_clicks[doc_id] += 1

    def save_query_terms(self, terms)->int:
        print(self)
        return random.randint(0, 100000)



class ClickedDoc:
    """
    A helper class for serializing clicked document data.
    """
    def __init__(self, doc_id, description, counter):
        self.doc_id = doc_id
        self.description = description
        self.counter = counter

    def to_json(self):
        return self.__dict__

    def __str__(self):
        """
        Print the object content as a JSON string.
        """
        return json.dumps(self)
