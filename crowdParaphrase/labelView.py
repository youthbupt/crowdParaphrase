#coding=utf8
from HITModel.PhraseUtils import PhraseUtils
from HITModel.MongoUtils import MongoUtils
from django.http import HttpResponse
from django.shortcuts import render
from userViews import getUserObject
import json

CLUSTER_COUNT_EACH_TIME = 1

def getLabelPage(request):

    #print request.session
    if "user" not in request.session:
        return HttpResponse("Please log in first.")
    # res = {}
    res = getUserObject(request)
    if "clusterCount" not in request.session:
        request.session["clusterCount"] = 0
        request.session["cluster"] = []

    if request.session["clusterCount"] >= CLUSTER_COUNT_EACH_TIME:
        print request.session["cluster"]
        dbParaList, nlpCluster = PhraseUtils.getMatchHIT(request.session["cluster"])
        
        res["dbParaList"] = dbParaList
        res["nlpCluster"] = nlpCluster
        request.session["clusterCount"] = 0
        request.session["cluster"] = []
        return render(request, "matchPage.html", res)
    else:
        if "labledPhrase" not in request.session:
            request.session["labledPhrase"] = []

        # res = getUserObject(request)
        res["phraseList"] = PhraseUtils.getRandomHIT(request.session["labledPhrase"])
    
        return render(request, "labelPage.html", res)


def saveLabeledRes(request):
    user = None
    if "user" not in request.session:
        return HttpResponse("Please log in first.")

    user = MongoUtils.getUser(request.session["user"])
    if user == None:
        return HttpResponse("No such user!")
    labeledRes = None
    print request.method
    if request.method == "POST":
       labeledRes = request.POST.get("labeledRes", None)

    if labeledRes is None:
        return HttpResponse("No request data")
    res = json.loads(labeledRes)
    posIdList = PhraseUtils.insertLabeledRes(user, res)
    if "clusterCount" not in request.session:
        request.session["clusterCount"] = 0
        request.session["cluster"] = []
    request.session["cluster"] += posIdList
    request.session["clusterCount"] += 1
    return HttpResponse("success")

def saveMatchRes(request):
    user = None
    if "user" not in request.session:
        return HttpResponse("Please log in first.")
    user = MongoUtils.getUser(request.session["user"])
    if user == None:
        return HttpResponse("No such user!")
    if request.method == "POST":
       matchRes = request.POST.get("matchRes", None)

    if matchRes is None:
        return HttpResponse("No request data")
    print matchRes
    res = json.loads(matchRes)
    PhraseUtils.insertMatchRes(user, res)
    return HttpResponse("success")


