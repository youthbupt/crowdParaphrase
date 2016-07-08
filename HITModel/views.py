#coding=utf8
from django.shortcuts import render
from MongoUtils import MongoUtils
from django.http import HttpResponse
import re

MAX_DB_PHRASE = -1
MAX_NLP_EACH_DB_PHRASE = -1

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

def getTuple(s):
    prefix = "<http://dbpedia.org/resource/"
    idx = s.find(prefix)
    if idx == 0:
        return s[len(prefix): -1].strip()
    prefix = "<http://dbpedia.org/ontology/"
    idx = s.find(prefix)
    if idx == 0:
        return s[len(prefix): -1].strip()
    print "What's this?!", s

def InsertQALDPhrase(source, path):
    QALDPhraseDict = {}
    with open("/media/database/dbpedia_DKRL_7.txt") as fin:
        lines = re.split(r"[\r\n]", fin.read())
        for line in lines:
            if len(line) < 5: continue
            tup = line.split("\t")
            if len(tup) != 3: continue
            subj = getTuple(tup[0])
            relation = getTuple(tup[1])
            obj = getTuple(tup[2])
            if relation not in QALDPhraseDict:
                QALDPhraseDict[relation] = (subj, obj)
            """
            print "subject:", subj
            print "relation:", relation
            print "object:", obj
            print len(line.split("\t"))
            break
            """
    
    with open(path, "r") as paraFileIn:
        dbPhraseSet = set()
        nlpPhraseSet = set()
        dbCandSet = dict()
        paraLines = re.split(r"[\r\n]", paraFileIn.read())
        for line in paraLines[1:]:
            paras = line.split('\t')
            if len(paras) != 2 or len(paras[1]) > 40: continue
            db_phrase = paras[0]

            if db_phrase not in QALDPhraseDict:
                continue
            nlp_phrase = paras[1].replace(";", "").strip()
            # insert database paraphrase to Mongodb
            if db_phrase not in dbPhraseSet:
                subj, obj = QALDPhraseDict[db_phrase]
                is_exist, db_object = MongoUtils.getAndSetDBPhraseWithExample(source, db_phrase, subj, obj)
                if not is_exist:
                    if MAX_DB_PHRASE > 0 and len(dbPhraseSet) >= MAX_DB_PHRASE:
                        break

                print 'Have inserted database phrase "%s":' % db_phrase
                dbPhraseSet.add(db_phrase)

                # if this database paraphrase is not in Mongodb yet, generate the candidates
            # insert nlp paraphrase to Mongodb
            if nlp_phrase not in nlpPhraseSet:
                flag, nlp_object = MongoUtils.getAndSetNLPPhrase(nlp_phrase)
                nlpPhraseSet.add(nlp_phrase)
                if not is_exist:
                    if db_object not in dbCandSet:
                        dbCandSet[db_object] = []
                    if MAX_NLP_EACH_DB_PHRASE > 0 and \
                    len(dbCandSet[db_object]) >= MAX_NLP_EACH_DB_PHRASE:
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


def InsertQALDPhraseFromFile():
    fileInfo = [("dbpedia", "/media/database/patty-dataset/dbpedia-relation-paraphrases.txt")]
    for (source, path) in fileInfo:
        InsertQALDPhrase(source, path)

def cleanAndInsert():
    cleanParaphraseDatabase()
    InsertFromFile()

if __name__ == "__main__":
    InsertQALDPhraseFromFile()

# Create your views here.
