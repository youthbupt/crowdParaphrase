#coding=utf8
from HITModel.PhraseUtils import PhraseUtils
from django.http import HttpResponse
from django.shortcuts import render

def getLabelPage(request):

    print request.session
    if "user" not in request.session:
        return HttpResponse("Please log in first.")

    if "labledPhrase" not in request.session:
        request.session["labledPhrase"] = []

    res = {}
    res["phraseList"] = PhraseUtils.getRandomHIT(request.session["labledPhrase"])
    
    return render(request, "labelPage.html", res)