#coding = utf8
from model import User

class UserUtils():
    @staticmethod
    def userRegister(username, password, mail):
        print "%s tries to login or register" % username
        user_object = User.objects(uname = username)
        if len(user_object) == 0:
            try:
                user_object = User(ID = User.objects.count() + 1, uname = username, mail = mail, \
                    password = password, confidence = 0.8, level = 0, taskCount = 0)
            except Exception as e:
                print e
                return 0
            user_object.save()
            print "A new user %s has just registered" % username
            return 1
        else:
            print "Username %s exists!" % username
            return 2

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

if __name__ == "__main__":
    print "user utils!"