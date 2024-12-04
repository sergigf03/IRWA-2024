import os
from json import JSONEncoder
import time



# pip install httpagentparser
import httpagentparser  # for getting the user agent as json
import nltk
from flask import Flask, render_template, session, jsonify
from flask import request

from myapp.analytics.analytics_data import AnalyticsData, ClickedDoc
from myapp.search.load_corpus import load_corpus
from myapp.search.objects import Document, StatsDocument
from myapp.search.search_engine import SearchEngine


# *** for using method to_json in objects ***
def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)


_default.default = JSONEncoder().default
JSONEncoder.default = _default

# end lines ***for using method to_json in objects ***

# instantiate the Flask application
app = Flask(__name__)

# random 'secret_key' is used for persisting data in secure cookie
app.secret_key = 'afgsreg86sr897b6st8b76va8er76fcs6g8d7'
# open browser dev tool to see the cookies
app.session_cookie_name = 'IRWA_SEARCH_ENGINE'

# instantiate our search engine
search_engine = SearchEngine()

# instantiate our in memory persistence
analytics_data = AnalyticsData()

# print("current dir", os.getcwd() + "\n")
# print("__file__", __file__ + "\n")
full_path = os.path.realpath(__file__)
path, filename = os.path.split(full_path)
# print(path + ' --> ' + filename + "\n")
# load documents corpus into memory.
file_path = path + "/farmers-protest-tweets.json"

# file_path = "../../tweets-data-who.json"
corpus = load_corpus(file_path)
#print("loaded corpus. first elem:", list(corpus.values())[0])

# Home URL "/"
@app.route('/')
def index():
    print("starting home url /...")

    # flask server creates a session by persisting a cookie in the user's browser.
    # the 'session' object keeps data between multiple requests
    session['some_var'] = "IRWA 2021 home"

    user_agent = request.headers.get('User-Agent')
    print("Raw user browser:", user_agent)

    user_ip = request.remote_addr
    agent = httpagentparser.detect(user_agent)

    
    session_info = {
        'browser': agent['browser']['name'],
        'os': agent['os']['name'],
        'ip': user_ip,
        'country': 'Spain',  
        'start_time': time.time()  # Timestamp for when the session started
    }
    
    # Save session info in analytics_data
    if session['some_var'] not in analytics_data.fact_sessions:
        analytics_data.fact_sessions[session['some_var']] = session_info

    print("Remote IP: {} - JSON user browser {}".format(user_ip, agent))

    print(session)
    return render_template('index.html', page_title="Welcome")


@app.route('/search', methods=['POST'])
def search_form_post():
    search_query = request.form['search-query']

    session['last_search_query'] = search_query

    search_id = analytics_data.save_query_terms(search_query)

    # Save query terms and their timestamp
    if search_query not in analytics_data.fact_queries:
        analytics_data.fact_queries[search_query] = {
            'terms': search_query.split(" "),
            'num_terms': len(search_query.split(" ")),
            'timestamp': time.time(),  # Timestamp of when the search happened
            'count': 1
        }
    else:
        analytics_data.fact_queries[search_query]['count'] += 1

    results = search_engine.search(search_query, search_id, corpus)

    found_count = len(results)
    session['last_found_count'] = found_count

    print(session)
    return render_template('results.html', results_list=results, page_title="Results", found_counter=found_count)


@app.route('/doc_details', methods=['GET'])
def doc_details():
    # getting request parameters:
    # user = request.args.get('user')

    print("doc details session: ")
    print(session)

    res = session["some_var"]

    print("recovered var from session:", res)

    # get the query string parameters from request
    clicked_doc_id = request.args["id"]
    #p1 = int(request.args["search_id"])  # transform to Integer
    #p2 = int(request.args["param2"])  # transform to Integer
    print("click in id={}".format(clicked_doc_id))
    result = corpus.get(int(clicked_doc_id))

    
    # store data in statistics table 1
    if clicked_doc_id in analytics_data.fact_clicks.keys():
        analytics_data.fact_clicks[clicked_doc_id] += 1
    else:
        analytics_data.fact_clicks[clicked_doc_id] = 1

    print("fact_clicks count for id={} is {}".format(clicked_doc_id, analytics_data.fact_clicks[clicked_doc_id]))

    return render_template('doc_details.html', result = result)


@app.route('/stats', methods=['GET'])
def stats():
    """
    Show simple statistics for clicks, queries, sessions
    """
    docs = []
    query_stats = []
    session_stats = []

    # Process clicks data
    for doc_id in analytics_data.fact_clicks:
        row: Document = corpus[int(doc_id)]
        count = analytics_data.fact_clicks[doc_id]
        doc = StatsDocument(row.id, row.title, row.description, row.doc_date, row.url, count)
        docs.append(doc)

    # Simulate sort by ranking for clicks (most clicked first)
    docs.sort(key=lambda doc: doc.count, reverse=True)

    # Process queries data
    for query_id, query_info in analytics_data.fact_queries.items():
        query_stat = {
            'query_id': query_id,
            'terms': query_info['terms'],
            'num_terms': query_info['num_terms'],
            'timestamp':  time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(query_info['timestamp'])),
            'count': query_info['count']
        }
        query_stats.append(query_stat)

    # Process session data
    for session_id, session_info in analytics_data.fact_sessions.items():
        session_stat = {
            'session_id': session_id,
            'browser': session_info['browser'],
            'os': session_info['os'],
            'ip': session_info['ip'],
            'country': session_info['country'],
            'start_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(session_info['start_time']))
        }
        session_stats.append(session_stat)


    # Render the statistics page with all the data
    return render_template('stats.html', clicks_data=docs, query_stats=query_stats, 
                           session_stats=session_stats)



@app.route('/dashboard', methods=['GET'])
def dashboard():
    visited_docs = []

    # Collect clicked documents and their click counts
    for doc_id in analytics_data.fact_clicks.keys():
        d: Document = corpus.get(int(doc_id))
        if d:
            count = analytics_data.fact_clicks[doc_id]
            doc = ClickedDoc(doc_id, d.description, count)
            visited_docs.append(doc)
            visited_docs =jsonify([doc.to_json() for doc in visited_docs]).json

    # Collect query statistics
    query_stats = []
    for query_id, query_info in analytics_data.fact_queries.items():
        query_stat = {
            'query_id': query_id,
            'terms': ', '.join(query_info['terms']),
            'num_terms': query_info['num_terms'],
            'timestamp': query_info['timestamp']
        }
        query_stats.append(query_stat)

    # Collect session statistics
    session_stats = []
    for session_id, session_info in analytics_data.fact_sessions.items():
        session_stat = {
            'session_id': session_id,
            'browser': session_info['browser'],
            'os': session_info['os'],
            'ip': session_info['ip'],
            'country': session_info['country'],
            'start_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(session_info['start_time']))
        }
        session_stats.append(session_stat)

    # Render the dashboard template with the necessary data
    return render_template('dashboard.html', visited_docs=visited_docs, query_stats=query_stats, session_stats=session_stats)


@app.route('/sentiment')
def sentiment_form():
    return render_template('sentiment.html')


@app.route('/sentiment', methods=['POST'])
def sentiment_form_post():
    text = request.form['text']
    nltk.download('vader_lexicon')
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    sid = SentimentIntensityAnalyzer()
    score = ((sid.polarity_scores(str(text)))['compound'])
    return render_template('sentiment.html', score=score)


if __name__ == "__main__":
    app.run(port=8088, host="0.0.0.0", threaded=False, debug=True)
