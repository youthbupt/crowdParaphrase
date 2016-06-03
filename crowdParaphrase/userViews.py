#coding=utf8
from django.shortcuts import render
from django.http import HttpResponse, Http404
from HITModel.MongoUtils import MongoUtils

def getLabelPage(request):
	print request.session
	if "user" in request.session:
		return render(request, "labelPage.html")
	else:
		return HttpResponse("Please log in first.")

def userLogout(request):

	if "user" in request.session:
		print "user %s tries to logout" % request.session["user"]
		del request.session["user"]
	return HttpResponse("success")

def getUserObject(request):
	user = None
	if "user" in request.session:
		user = MongoUtils.getUser(request.session["user"])
	return user

def getHomePage(request):
	res = {}
	user = getUserObject(request)

	if user is not None:
		res['hasLogin'] = True
		res["username"] = user.uname
		res["confidence"] = user.confidence
		res["level"] = user.level 
		res["taskCount"] = user.taskCount
	else:
		res['hasLogin'] = False
	return render(request, "home.html", res)

def checkLogin(request):
	if "user" in request.session:
		return HttpResponse("success")
	else:
		return HttpResponse("failed")


def userLogin(request):
	if "user" in request.session:
		return HttpResponse("User is already login")
	else:
		if request.method == "POST":
			username = request.POST.get("user", None)
		else:
			username = request.GET.get("user", None)

		if username == None:
			return HttpResponse("Username cannot be none!")
		username = username.strip()
		if len(username) < 1 or username.find(' ') != -1:
			return HttpResponse("Illegal username!")
		else:
			flag = userRegister(username)
			request.session["user"] = username
			return HttpResponse("success")

def userRegister(username):
	flag, userObject = MongoUtils.userRegister(username)
	return flag


