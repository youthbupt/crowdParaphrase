#coding=utf8
from HITModel.PhraseUtils import PhraseUtils
from HITModel.MongoUtils import MongoUtils
from django.http import HttpResponse
from django.shortcuts import render
from userViews import getUserObject
import json
import re

CLUSTER_COUNT_EACH_TIME = 1


stopWordSet = set()

def getStopWords():
    with open("/media/coding/crowdParaphrase/stopwords.txt") as fin:
        lines = re.split(r"[\r\n]", fin.read())
        for l in lines:
            if len(l) < 1:continue
            stopWordSet.add(l.strip())
getStopWords()


def phraseFilter(s):
    s = re.sub(r"\[\[\w*\]\]", " ", s).strip()
    s = re.sub(r" {2,}", " ", s)
    wordList = s.split(' ')
    filteredWordList = []
    for word in wordList:
        if len(word) > 0 and word not in stopWordSet:
            filteredWordList.append(word)
    return " ".join(filteredWordList).strip()


def isSame(s1, s2):
    #print "before:", s1, "  &&  ", s2
    s1 = phraseFilter(s1)
    s2 = phraseFilter(s2)
    """
    if "involved" in s1 and "involved" in s2:
        print s1, "@@@@@", s2
    """
    #print "after:", s1, "  &&  ", s2, " && ", s1 == s2
    return s1 == s2

def getCluster(randomHIT):
    candDict = {}
    for dbId, nlpId, nlpName in randomHIT:
        if dbId not in candDict:
            candDict[dbId] = []
        hashFind = False
        clen = len(candDict[dbId])
        for i in xrange(clen):
            if len(candDict[dbId][i]) > 5: continue
            if isSame(nlpName, candDict[dbId][i][0][1]):
                hashFind = True
                candDict[dbId][i].append((nlpId, nlpName))
                break
        if not hashFind:
            candDict[dbId].append([])
            candDict[dbId][clen].append((nlpId, nlpName))
    candRes = []
    for db, candList in candDict.items():
        for cand in candList:
            candRes.append((db, cand))
            if len(candRes) > 15: break
    return candRes
#def cluster()

def getLabelPage(request):

    #print request.session
    if "user" not in request.session:
        return HttpResponse("Please log in first.")
    # res = {}

    res = getUserObject(request)
    print res
    if "clusterCount" not in request.session:
        request.session["clusterCount"] = 0
        request.session["cluster"] = []

    # print "hahahahaha", request.session["clusterCount"]
    if request.session["clusterCount"] >= CLUSTER_COUNT_EACH_TIME:
        # print request.session["cluster"]
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
        randomHIT = PhraseUtils.getRandomHIT(request.session["labledPhrase"])
        # print "123:", randomHIT
        res["phraseList"] = getCluster(randomHIT)
        # print res["phraseList"]
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


