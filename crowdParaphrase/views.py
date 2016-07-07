#coding=utf8
from django.shortcuts import render
from django.http import HttpResponse, Http404

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

        res["phraseList"] = PhraseUtils.getRandomHIT(request.session["labledPhrase"])
    
        return render(request, "labelPage.html", res)

def getHomePage(request):
    return render(request, "home.html")
