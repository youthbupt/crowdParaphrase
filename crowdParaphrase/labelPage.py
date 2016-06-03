#coding=utf8
from django.shortcuts import render

def getLabelPage(request):
	return render(request, "labelPage.html")	