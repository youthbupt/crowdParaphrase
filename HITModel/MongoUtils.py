#coding=utf8
from model import NLPParaphrase as nlpPhrase, DatabaseParaphrase as dbPhrase,\
ParaphraseCandidate as paraCand, MatchPair as matchPair
from mongoengine import *

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
    def insertNLPCluster(cluster):
        nlpCluster = NLPPhraseCluster(ID = NLPPhraseCluster.objects.count() + 1, \
            cluster = cluster)
        nlpCluster.save()
        return nlpCluster

    @staticmethod
    def insertPhraseCand(dbPhrase, candidates):
        phraseCand = paraCand(ID = paraCand.objects.count() + 1, \
            dbPhrase = dbPhrase, candidates = candidates)
        phraseCand.save()
        return phraseCand

    @staticmethod
    def cleanAllPhrase():
        NLPPhraseCluster.objects().delete()
        paraCand.objects().delete()
        nlpPhrase.objects().delete()
        dbPhrase.objects().delete()


    @staticmethod
    def transInt2IntField(intArr):
        res = []
        for i in intArr:
            now = IntField()
            now.value = i
            res.append(now)
        return res

    @staticmethod
    def transFloat2FloatField(floatArr):
        res = []
        for i in floatArr:
            now = FloatField()
            now.value = i
            res.append(now)
        return res
