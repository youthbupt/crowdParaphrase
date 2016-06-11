#coding=utf8
from HITModel.PhraseUtils import PhraseUtils
from HITModel.MongoUtils import MongoUtils
from django.http import HttpResponse
from django.shortcuts import render
import json

def getLabelPage(request):

    #print request.session
    if "user" not in request.session:
        return HttpResponse("Please log in first.")

    if "labledPhrase" not in request.session:
        request.session["labledPhrase"] = []

    res = {}
    res["phraseList"] = PhraseUtils.getRandomHIT(request.session["labledPhrase"])
    
    return render(request, "labelPage.html", res)


def saveLabeledRes(request):
    user = None
    if "user" not in request.session:
        return HttpResponse("Please log in first.")

    user = MongoUtils.getUser(request.session["user"])
    if user == None:
        return HttpResponse("No such user!")

    if request.method == "POST":
       labeledRes = request.POST.get("labledRes", None)
    if labledRes is None:
        return HttpResponse("No request data")
    res = json.loads(labledRes)
    PhraseUtils.insertLabeledRes(res)

