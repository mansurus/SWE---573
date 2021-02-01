import nltk
import praw
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import auth
import requests
import json
import os
from rest_framework import views
from rest_framework.response import Response
from collections import OrderedDict
from psaw import PushshiftAPI
import datetime as dt
from django.contrib import messages  
import wikipedia
import vader_sentiment
import traceback
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

reddit = praw.Reddit(client_id="TPb9LNkPhytKZQ", client_secret="jEDwDAF3_HLU9juAcaD_LpGL6QX9BA", user_agent="covidWebApp")


sid = SentimentIntensityAnalyzer()


def getNegativeProbs(text):
   return sid.polarity_scores(text)['neg']

def getNeutralProbs(text):
   return sid.polarity_scores(text)['neu']

def getPositiveProbs(text):
   return sid.polarity_scores(text)['pos']


def getKeywordBasedComments(text):
    data = []
    url_ = "https://api.pushshift.io/reddit/search/comment/?q="+text+"&subreddit=coronavirus&size=100&fields=body,author"
    reddit_request = requests.get(url=url_)
    json_response = reddit_request.json() 
    for submission in json_response["data"]:
        comment=submission['body']
        commentASCII = comment.encode(encoding='ascii', errors='ignore').decode()
        data.append(commentASCII)
    
    return data
        
    


def processFetchedComments(comment, negativeComments, neutralComments, positiveComments):
    if comment is None:
        return ''

    text = comment

    neg = getNegativeProbs(text)
    neu = getNeutralProbs(text)
    pos = getPositiveProbs(text)

    prob = [neg, neu, pos]

    if neg == max(prob):
        negativeComments.append(text)
    if neu == max(prob):
        neutralComments.append(text)
    if pos == max(prob):
        positiveComments.append(text)

    return [negativeComments, neutralComments, positiveComments]

def nltkView(request, **kwargs):
    keyword=""

    if request.method=='POST':
        try:
            keyword = request.POST['searchForAnalyze']
        except:
            messages.add_message(request, messages.ERROR, 'Please enter correct values!')
            return redirect("erroranalyze")
    comments = getKeywordBasedComments(keyword)

    neg = []
    neu = []
    pos = []

    processedComments = []

    newNeg = []
    newNeu = []
    newPos = []

    lengthOfNeg = 0
    lengthOfNeu = 0
    lengthOfPos = 0
    for i in range(len(comments)):
        processedComments = (processFetchedComments(comments[i], neg, neu, pos))

    for i in range(len(processedComments)):
        if i == 0:
            for j in range(len(processedComments[i])):
                lengthOfNeg +=1
                if processedComments[i][j][0] == "&":
                    continue
                else:
                    newNeg.append(processedComments[i][j])
                   
        if i == 1: 
            for j in range(len(processedComments[i])):
                lengthOfNeu +=1
                if processedComments[i][j][0] == "&":
                    continue
                else:
                    newNeu.append(processedComments[i][j])
                   
            
        if i == 2:
            for j in range(len(processedComments[i])):
                lengthOfPos +=1
                if processedComments[i][j][0] == "&":
                    continue
                else:
                    newPos.append(processedComments[i][j])
                   

        context2 = {"negLength":lengthOfNeg,
                    "neuLength":lengthOfNeu,
                    "posLength":lengthOfPos}
    if len(comments) == 0 :
        return redirect("erroranalyze")
    else:
        return render(request, "pages/analyze.html", {
            "newNeg":newNeg,
            "newNeu":newNeu,
            "newPos":newPos,
            'context2': context2,
        })

def errorAnalyze(request):
    return render(request, "pages/404analyze.html")

