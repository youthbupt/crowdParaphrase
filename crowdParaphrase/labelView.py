#coding=utf8
from HITModel.PhraseUtils import PhraseUtils
from HITModel.MongoUtils import MongoUtils
from django.http import HttpResponse
from django.shortcuts import render
from userViews import getUserObject
import json

def getLabelPage(request):

    #print request.session
    if "user" not in request.session:
        return HttpResponse("Please log in first.")

    if "labledPhrase" not in request.session:
        request.session["labledPhrase"] = []

    res = getUserObject(request)
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
    PhraseUtils.insertLabeledRes(res)
    return HttpResponse("Success")

