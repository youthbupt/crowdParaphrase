#coding=utf8
from django.shortcuts import render
from django.http import HttpResponse, Http404
from HITModel.MongoUtils import MongoUtils
from HITModel.UserUtils import UserUtils
import re

def getLabelPageTest(request):
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
        user = UserUtils.getUser(request.session["user"])
    res = {}
    if user is not None:
        res['hasLogin'] = True
        res["username"] = user.uname
        res["confidence"] = user.confidence
        res["level"] = user.level 
        res["taskCount"] = user.taskCount
    else:
        res['hasLogin'] = False
    return res


def checkLogin(request):
    # print request.session["user"]
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
            password = request.POST.get("password", None)
        else:
            username = request.GET.get("user", None)
            password = request.GET.get("password", None)

        if username == None:
            return HttpResponse("Username cannot be none!")
        username = username.strip()
        if len(username) < 1 or username.find(' ') != -1:
            return HttpResponse("Illegal username!")
        flag = UserUtils.userLogin(username, password)
        if flag == 1:
            request.session["user"] = username
            return HttpResponse("success")
        if flag == 0:
            return HttpResponse("no such user!")
        
        if flag == 2:
            return HttpResponse("password is incorrect!")

def userRegister(request):
    if request.method == "POST":
        username = request.POST.get("user", None)
        password = request.POST.get("password", None)
        mail = request.POST.get("mail", None)
    else:
        username = request.GET.get("user", None)
        password = request.GET.get("password", None)
        mail = request.POST.get("mail", None)

    if username is None:
        return HttpResponse("User name cannot be null")
    if password is None:
        return HttpResponse("Password cannot be null")
    if mail is None:
        return HttpResponse("Email address cannot be null")
    if len(username) < 5:
        return HttpResponse("User name must be longer than 5 charactors!")
    if len(username) >= 20:
        return HttpResponse("User name must be less than 20 charactors!")
    res = re.match(r'^(\w)+(\.\w+)*@(\w)+((\.\w+)+)$', mail)
    if res is None:
        return HttpResponse("Please input a valid email address!")
    
    resState = UserUtils.userRegister(username, password, mail)
    if resState == 1:
        request.session["user"] = username
        return HttpResponse("success")

    if resState == 2:
        return HttpResponse("User name already exists!")

    return HttpResponse("Register failed! Please try again")


