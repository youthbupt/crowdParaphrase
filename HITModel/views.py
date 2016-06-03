#coding=utf8
from django.shortcuts import render
from MongoUtils import MongoUtils
import django.http.HttpResponse
import re

def InsertToDatabase(source, path):
	with open(path, "r") as paraFileIn:
		dbPhraseSet = set()
		nlpPhraseSet = set()
		dbCandSet = dict()
		paraLines = re.split(r"[\r\n]", paraFileIn.read())
		for line in paraLines[1:]:
			paras = line.split('\t')
			if len(paras) != 2 or len(paras[1]) > 40: continue
			db_phrase = paras[0]
			nlp_phrase = paras[1].replace(";", "").strip()

			# insert database paraphrase to Mongodb
			if db_phrase not in dbPhraseSet:
				
				is_exist, db_object = MongoUtils.getAndSetDBPhrase(source, db_phrase)
				dbPhraseSet.add(db_phrase)

				# if this database paraphrase is not in Mongodb yet, generate the candidates

			# insert nlp paraphrase to Mongodb
			if nlp_phrase not in nlpPhraseSet:
				flag, nlp_object = MongoUtils.getAndSetNLPPhrase(nlp_phrase)
				nlpPhraseSet.add(nlp_phrase)
				if not is_exist:
					if db_object not in dbCandSet:
						dbCandSet[db_object] = []
					dbCandSet[db_object].append(nlp_object)

				
		#insert database paraphrase's candidates
		for db_phrase, cand_list in dbCandSet:
			MongoUtils.insertCandidate(db_phrase, cand_list)
			
def InsertFromFile(request):
	fileInfo = [("dbpedia", "/media/database/patty-dataset/dbpedia-relation-paraphrases.txt"), 
	("yago", "/media/database/patty-dataset/yago-relation-paraphrases.txt")]
	for (source, path) in fileInfo:
		InsertToDatabase(source, path)
	return HTTPResponse("Success!")

def cleanParaphraseDatabase(request):
	MongoUtils.cleanAllPhrase()
	return HTTPResponse("Delete all paraphrase!")

# Create your views here.
