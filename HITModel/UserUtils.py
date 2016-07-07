#coding = utf8
from model import User

class UserUtils():
    @staticmethod
    def userRegister(username, password):
        print "%s tries to login or register" % username
        user_object = User.objects(uname = username)
        if len(user_object) == 0:
            user_object = User(ID = User.objects.count() + 1, uname = username, password = password, confidence = 0.0, level = 0, taskCount = 0)
            user_object.save()
            print "A new user %s has just registered" % username
            return False, user_object
        else:
            print "User %s has logged in" % username
            return True, user_object

    @staticmethod
    def userLogin(username, password):
    	user_object = User.objects(uname = username)
    	if len(user_object) == 0:
    		return 0
    	user = user_object[0]
    	if user.password == password:
    		return 1
    	return 2

    @staticmethod
    def removeAllUsers():
        User.objects().delete()


    @staticmethod
    def getUser(username):
        user_object = User.objects(uname = username)
        if len(user_object) == 0:
            return None
        return user_object[0]