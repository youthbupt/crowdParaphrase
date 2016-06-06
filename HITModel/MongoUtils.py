#coding=utf8
from model import NLPParaphrase as nlpPhrase, DatabaseParaphrase as dbPhrase,\
ParaphraseCandidate as paraCand, MatchPair as matchPair, User 

class MongoUtils():
	@staticmethod
	def getAndSetDBPhrase(source, db_phrase):
		db_objects = dbPhrase.objects(source = source, pname = db_phrase)
		if len(db_objects) > 0:
			db_object = db_objects[0]
			flag = True
		else:
			db_object = dbPhrase(ID = dbPhrase.objects.count() + 1, source = source, pname = db_phrase)
			db_object.save()
			flag = False
		return flag, db_object

	@staticmethod
	def getAndSetNLPPhrase(nlp_phrase):
		nlp_objects = nlpPhrase.objects(pname = nlp_phrase)
		if len(nlp_objects) > 0:
			nlp_object = nlp_objects[0]
			flag = True
		else:
			nlp_object = nlpPhrase(ID = nlpPhrase.objects.count() + 1, pname = nlp_phrase)
			nlp_object.save()
			flag = False
		return flag, nlp_object

	@staticmethod
	def insertCandidate(db, cand_list, confidence = 1.0):
		match_pairs = []
		for cand in cand_list:
			# print 233,
			match_pairs.append(matchPair(NLPParaphrase = cand, confidence = confidence))
		cand_object = paraCand(ID = paraCand.objects.count() + 1, DbpediaParaphrase = db, candidates = match_pairs)
		cand_object.save()

	@staticmethod
	def userRegister(username):
		print "%s tries to login or register" % username
		user_object = User.objects(uname = username)
		if len(user_object) == 0:
			user_object = User(ID = User.objects.count() + 1, uname = username, confidence = 0.0, level = 0, taskCount = 0)
			user_object.save()
			print "A new user %s has just registered" % username
			return False, user_object
		else:
			print "User %s has logged in" % username
			return True, user_object

	@staticmethod
	def cleanAllPhrase():
		paraCand.objects().delete()
		nlpPhrase.objects().delete()
		dbPhrase.objects().delete()

	@staticmethod
	def removeAllUsers():
		User.objects().delete()


	@staticmethod
	def getUser(username):
		user_object = User.objects(uname = username)
		if len(user_object) == 0:
			return None
		return user_object[0]
