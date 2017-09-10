from flask import Flask, redirect, render_template, request, url_for

import helpers
from analyzer import Analyzer
import os
import sys

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():

    # validate screen_name
    screen_name = request.args.get("screen_name", "")
    if not screen_name:
        return redirect(url_for("index"))

    # get screen_name's tweets
    tweets = helpers.get_user_timeline(screen_name, count = 100)
    if not tweets:
        return redirect(url_for("index"))

    # absolute paths to lists
    positive_words = os.path.join(sys.path[0], "positive-words.txt")
    negative_words = os.path.join(sys.path[0], "negative-words.txt")

    # instantiate analyzer
    analyzer = Analyzer(positive_words, negative_words)
    
    # Analyze tweets
    pos_count = 0.0 # positive tweets
    neg_count = 0.0 # negative tweets
    neutral_count = 0.0 # neutral tweets
    for tweet in tweets:
        score = analyzer.analyze(tweet)
        if score > 0.0:
            pos_count += 1
        elif score < 0.0:
            neg_count += 1
        else:
            neutral_count += 1 
            
    # normalize if tweets are less than 100        
    total_tweet = len(tweets)        
    if total_tweet < 100:
        pos_count = (pos_count / total_tweet)*100
        neg_count = (neg_count / total_tweet)*100
        neutral_count = (neutral_count / total_tweet)*100
        
    positive, negative, neutral = pos_count, neg_count, neutral_count
    
    # generate chart
    chart = helpers.chart(positive, negative, neutral)

    # render results
    return render_template("search.html", chart=chart, screen_name=screen_name)
