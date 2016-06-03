#coding=utf8
from django.shortcuts import render
from django.http import HttpResponse, Http404

def getLabelPage(request):
	print request.session
	if "username" in request.session:
		return render(request, "labelPage.html")
	else:
		return HttpResponse("Please log in first.")

def userLogout(request):
	if "username" in request.session:
		del request.session["username"]

def getHomePage(request):
	return render(request, "home.html")

def checkLogin(request):
	if "username" in request.session:
		return HttpResponse("success")
	else:
		return HttpResponse("failed")


def userLogin(request):
	if "username" in request.session:
		return HttpResponse("User is already login")
	else:
		if request.method == "POST":
			username = request.POST.get("username", None)
		else:
			username = request.GET.get("username", None)

		if username == None:
			raise Http404("Username cannot be none!")
		username = username.strip()
		print username
		if len(username) < 1 or username.find(' ') != -1:
			raise Http404("Illegal username!")
		else:
			request.session["username"] = username
			return HttpResponse("success")
