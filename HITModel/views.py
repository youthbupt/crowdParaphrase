#coding=utf8
from django.shortcuts import render
from MongoUtils import MongoUtils
from django.http import HttpResponse
import re

MAX_DB_PHRASE = 5
MAX_NLP_EACH_DB_PHRASE = 20

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
                if not is_exist:
                    if len(dbPhraseSet) >= MAX_DB_PHRASE:
                        break
                dbPhraseSet.add(db_phrase)

                # if this database paraphrase is not in Mongodb yet, generate the candidates
            # insert nlp paraphrase to Mongodb
            if nlp_phrase not in nlpPhraseSet:
                flag, nlp_object = MongoUtils.getAndSetNLPPhrase(nlp_phrase)
                nlpPhraseSet.add(nlp_phrase)
                if not is_exist:
                    if db_object not in dbCandSet:
                        dbCandSet[db_object] = []
                    if len(dbCandSet[db_object]) >= MAX_NLP_EACH_DB_PHRASE:
                        continue
                    dbCandSet[db_object].append(nlp_object)

                
        #insert database paraphrase's candidates
        for db_phrase, cand_list in dbCandSet.items():
            # print db_phrase
            # print cand_list
            MongoUtils.insertCandidate(db_phrase, cand_list)
            
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
    print "remove all paraphrase!"
    if request is not None:
        return HttpResponse("Delete all paraphrase!")

def removeAllUsers(request = None):
    MongoUtils.removeAllUsers()
    print "remove all users' profile!"
    if request is not None:
        return HttpResponse("Success!")

if __name__ == "__main__":
    cleanParaphraseDatabase()
    InsertFromFile()

# Create your views here.
