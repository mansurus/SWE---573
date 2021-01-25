from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import auth
import requests
import praw
import json
import os
from rest_framework import views
from rest_framework.response import Response
from collections import OrderedDict
from psaw import PushshiftAPI
import datetime as dt
from django.contrib import messages  
import wikipedia

reddit = praw.Reddit(client_id="TPb9LNkPhytKZQ", client_secret="jEDwDAF3_HLU9juAcaD_LpGL6QX9BA", user_agent="covidWebApp")
api = PushshiftAPI(reddit)


# get posts
def redditsearch(request):
        data = []
        coronavirus_subreddit = reddit.subreddit("coronavirus").hot(limit=50)
        for submission in coronavirus_subreddit:
            if submission.stickied == False:
                data.append(submission)
        context = {'data':data}
        return render(request, 'pages/result.html', context)



def vaccineSub(request, **kwargs):
    data = []
    url = f"https://api.pushshift.io/reddit/search/submission/?q=vaccine&subreddit=coronavirus"
    payload =kwargs
    reddit_request = requests.get(url, params=payload)
    json_response = reddit_request.json() 
    for submission in json_response["data"]:
        data.append(submission)

    def sort_score(json):
        try:
            return int(json_response['score'])
        except KeyError:
            return 0


    data.sort(key=sort_score,reverse=True)
    context = {'data':data}

    return render(request, 'pages/vaccine.html', context)




def searchKeyword(request, **kwargs):
    dataNew = []
    linkKeyword= "https://api.pushshift.io/reddit/search/submission/?q="
    linkDays = "&subreddit=coronavirus&after="
    if request.method=='POST':
        try:
            keyword = request.POST['keyword']
            day = request.POST['dayNum']
            int(day)
        except ValueError:
            messages.add_message(request, messages.ERROR, 'Please enter correct values!')
            return redirect("vaccine")
            
    url = linkKeyword+keyword+linkDays+day+"d"
    payload =kwargs
    reddit_request1 = requests.get(url, params=payload)
    json_response1 = reddit_request1.json() 
    for submission in json_response1["data"]:
        dataNew.append(submission)

    def sort_score(json):
        try:
            return int(json_response1['score'])
        except KeyError:
            return 0


    dataNew.sort(key=sort_score,reverse=True)
    context1 = {'data':dataNew}
    if len(dataNew)==0:
        return redirect("error")
    return render(request, 'pages/search.html', context1)

# https://api.pushshift.io/reddit/search/submission/?q=mask&subreddit=coronavirus&after=7d


def wikiResult(request, **kwargs):
    if request.method=="POST":
        try:
            searchWord = request.POST['searchWord']
            searchContent = wikipedia.summary(searchWord)
            searchTitle = wikipedia.page(searchWord)
            wikiContext={"wikiContent":searchContent,"wikiTitle":searchTitle}
            return render(request, 'pages/wikiresult.html', wikiContext)
        except:
            return redirect("error2")
          
            
            
        
            
        


def posts(request, id):
    # post_id = request.GET.get('id')
    data = reddit.submission(id=id)
    if data.subreddit == 'coronavirus':
        context = {'data': data}
        return render(request, 'pages/eachpost.html', context)
    else:
        return render(request, 'pages/404.html')

# class ListJson(views.APIView):
#     def get(self, request):
#         data = []
#         coronavirus_subreddit = reddit.subreddit('coronavirus').hot(limit=50)
#         for submission in coronavirus_subreddit:
#             if submission.stickied == False:
#                 data.append([{
#                     "post_id": submission.id,
#                     "author": str(submission.author),
#                     "title": submission.title,
                   
#                 }])
#         return Response(data)

# class ListJsonById(views.APIView):
#     def get(self, request, id):
#         post_id = request.query_params.get('id')
#         coronavirus_data = reddit.submission(id=id)
#         if coronavirus_data.subreddit == 'coronavirus':
#             data = [{
#                 "post": coronavirus_data.selftext,
#                 "flair": coronavirus_data.link_flair_text,
#                 "upvote": coronavirus_data.score,
#             }]

#         return Response(data)

def errorPage(request):
    return render(request, "pages/404.html")
def errorWiki(request):
    return render(request, "pages/500.html")

