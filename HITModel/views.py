#coding=utf8
from django.shortcuts import render
from MongoUtils import MongoUtils
from django.http import HttpResponse
import re

MAX_DATABASE_PHRASE_NUM = 100
MAX_NLP_PHRASE_EACH_DB_NUM = 20

def phraseFilter(s, stopWord):
	s = re.sub(r"\[\[\w*\]\]", " ", s).strip()
	s = re.sub(r" {2,}", " ", s)
	wordList = s.split(' ')
	filteredWordList = []
	for word in wordList:
		if len(word) > 0 and word not in stopWord:
			filteredWordList.append(word)
	return " ".join(filteredWordList).strip()


def isSame(s1, s2, stopWordSet):
	#print "before:", s1, "  &&  ", s2
	s1 = phraseFilter(s1, stopWordSet)
	s2 = phraseFilter(s2, stopWordSet)
	"""
	if "involved" in s1 and "involved" in s2:
		print s1, "@@@@@", s2
	"""
	#print "after:", s1, "  &&  ", s2, " && ", s1 == s2
	return s1 == s2

def clusterPhrase(nlpObjList, stopWordSet):
	cluster = []
	clen = 0
	"""
	for phrase in nlpObjList:
		print phrase.pname, "#####",
	print
	"""
	for nlpObj in nlpObjList:
		hasFind = False
		for i in xrange(clen):
			same = isSame(cluster[i][0].pname, nlpObj.pname, stopWordSet)
			# print cluster[i][0].pname, " $$$$$$$$$ ", nlpObj.pname, "  ", same
			if same:
				hasFind = True
				cluster[i].append(nlpObj)
				break
		if not hasFind:
			cluster.append([])
			cluster[clen].append(nlpObj)
			clen += 1
	"""
	for clus in cluster:
		for phrase in clus:
			print phrase.pname, "@@@@",
		print
	"""
	return cluster

def InsertToDatabase(source, path):
	stopWordSet = set()
	with open("/media/coding/crowdParaphrase/stopwords.txt") as fin:
		lines = re.split(r"[\r\n]", fin.read())
		for l in lines:
			if len(l) < 1:continue
			stopWordSet.add(l.strip())


	with open(path, "r") as paraFileIn:
		dbPhraseSet = set()
		nlpPhraseSet = set()
		dbCandSet = dict()
		paraLines = re.split(r"[\r\n]", paraFileIn.read())
		phraseCandList = {}
		for line in paraLines[1:]:
			paras = line.split('\t')
			if len(paras) != 2 or len(paras[1]) > 40: continue
			db_phrase = paras[0]
			nlp_phrase = paras[1].replace(";", "").strip()
			"""
			if db_phrase not in phraseCandList:
				phraseCandList[db_phrase] = []
				print db_phrase, len(phraseCandList)
				
				continue
			"""

			# insert database paraphrase to Mongodb
			if db_phrase not in dbPhraseSet:
				
				is_exist, db_object = MongoUtils.getAndSetDBPhrase(source, db_phrase)
				dbPhraseSet.add(db_phrase)

				# if this database paraphrase is not in Mongodb yet, generate the candidates

			# insert nlp paraphrase to Mongodb
			if nlp_phrase not in nlpPhraseSet:
				is_exist, nlp_object = MongoUtils.getAndSetNLPPhrase(nlp_phrase)
				nlpPhraseSet.add(nlp_phrase)
				if not is_exist:
					if db_object not in dbCandSet:
						
						if len(dbCandSet) >= MAX_DATABASE_PHRASE_NUM:
							print "Has inserted %d paraphrase, stopping..." % MAX_DATABASE_PHRASE_NUM
							break
						dbCandSet[db_object] = []
					if len(dbCandSet[db_object]) >= MAX_NLP_PHRASE_EACH_DB_NUM:
						continue
					dbCandSet[db_object].append(nlp_object)

			# phraseCandList[db_phrase].append(nlp_phrase)

				
		#insert database paraphrase's candidates
		
		for db_phrase, cand_list in dbCandSet.items():
			clusteredCand = clusterPhrase(cand_list, stopWordSet)
			clusterList = []
			for cluster in clusteredCand:
				nlpCluster = MongoUtils.insertNLPCluster(cluster)
				clusterList.append(nlpCluster)
			MongoUtils.insertPhraseCand(db_phrase, clusterList)
			# print db_phrase
			# print cand_list
			pass
			# MongoUtils.insertCandidate(db_phrase, cand_list)
			
def InsertFromFile(request = None):
	
	fileInfo = [ ("yago", "/media/database/patty-dataset/yago-relation-paraphrases.txt")]
	"""
	fileInfo = [("dbpedia", "/media/database/patty-dataset/dbpedia-relation-paraphrases.txt"), 
	("yago", "/media/database/patty-dataset/yago-relation-paraphrases.txt")]
	"""
	for (source, path) in fileInfo:
		InsertToDatabase(source, path)
	print "insert all phrase information to database!"
	if request is not None:
		return HttpResponse("Success!")

def cleanParaphraseDatabase(request = None):
	MongoUtils.cleanAllPhrase()
	# print "remove all paraphrase!"
	if request is not None:
		return HttpResponse("Delete all paraphrase!")
	else:
		print "Delete all paraphrase!"

def removeAllUsers(request = None):
	MongoUtils.removeAllUsers()
	if request is not None:
		return HttpResponse("Success!")
	else:
		print "remove all users' profile!"

if __name__ == "__main__":
	cleanParaphraseDatabase()
	InsertFromFile()
	# cleanParaphraseDatabase()

# Create your views here.
