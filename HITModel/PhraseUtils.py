#coding=utf8
from MongoUtils import MongoUtils
from model import ParaphraseCandidate, NLPParaphrase, HITClusterPositiveRes, HITClusterNegativeRes
import random
from datetime import datetime

# global parameters
candPairLen = len(ParaphraseCandidate.objects)
# print "length of paraphrase candidates list: %d" % candPairLen

class PhraseUtils():

    @staticmethod
    def getRandomHIT(prevList, MAX_DB_PHRASE = 5, MAX_NLP_PHRASE = 20):
        NLPPhraseCount = 0
        selectedDict = dict()
        
        while (NLPPhraseCount < MAX_NLP_PHRASE):
            if len(selectedDict) == candPairLen:
                break
            nowCandId = random.randint(0, candPairLen)
            if nowCandId in selectedDict or nowCandId in prevList:
                continue
            nowCandList = ParaphraseCandidate.objects(ID = nowCandId)
            if nowCandList is None or len(nowCandList) == 0:
                continue
            nowCand = nowCandList[0]
            if prevList is None:
                prevList = []

            prevList.append(nowCandId)
            selectedDict[nowCandId] = []
            candLen = len(nowCand.candidates)
            if NLPPhraseCount + candLen <= MAX_NLP_PHRASE:
                for nlp_phrase in nowCand.candidates:
                    selectedDict[nowCandId].append(nlp_phrase)
                    #print nlp_phrase
                NLPPhraseCount += candLen
            else:
                cand = []
                for nlp_phrase in nowCand.candidates:
                    cand.append(nlp_phrase)
                random.shuffle(cand)
                i = 0
                while NLPPhraseCount < MAX_NLP_PHRASE:
                    i += 1
                    selectedDict[nowCandId].append(cand[i])
                    NLPPhraseCount += 1
            #print selectedDict[nowCandId]
        resList = []
        for db_id, cand_list in selectedDict.items():
            for cand in cand_list:
                resList.append((db_id, cand.NLPParaphrase.ID, cand.NLPParaphrase.pname))
        # print resList
        # print len(resList)
        return resList

    @staticmethod
    def getNLPPhrase(phraseId):
        phrase = NLPParaphrase.objects(ID = phraseId)
        if len(phrase) == 0:
            return None
        return phrase[0]

    @staticmethod
    def insertLabeledRes(user, cluster_list):

        for cluster in cluster_list:
            nowCluster = []
            dbParaCount = {}
            clusterLen = len(cluster)
            for nlpId, dbId in cluster:
                nlpId = int(nlpId)
                dbId = int(dbId)
                if nlpId is not None:
                    nowCluster.append(nlpId)
                if dbId not in dbParaCount:
                    dbParaCount[dbId] = 1.0 / clusterLen
                else:
                    dbParaCount[dbId] += 1.0 / clusterLen
            dbParaList = dbParaCount.items()
            posObj = HITClusterPositiveRes(ID = len(HITClusterPositiveRes.objects()) + 1, user = user, \
                dbPara = dbParaList, cluster = nowCluster, date = datetime.now())
            posObj.save()

        l = len(cluster_list)
        if l == 0: return
        for x in xrange(l):
            cluster = cluster_list[x]
            for phraseId in cluster:
                negPhrase = []
                for y in xrange(l):
                    if x == y:continue
                    neg_cluster = cluster_list[y]
                    for neg in neg_cluster:
                        negPhrase.append(neg)
                if len(negPhrase) > 0:
                    negObj = HITClusterNegativeRes(ID = len(HITClusterNegativeRes.objects() + 1), \
                        nlp_phrase = nlp_phrase, user = user, cluster = negPhrase, date = datetime.now())
                    negObj.save()

    @staticmethod
    def cleanLabeledRes():
        HITClusterPositiveRes.objects().delete()
        HITClusterNegativeRes.objects().delete()

def testGetRandomHIT():
    preSet = set()
    res = PhraseUtils.getRandomHIT(preSet)
    print res

def testSavedLabelRes():
    print "---------- positive clusters ------------"
    for pos_clusters in HITClusterPositiveRes.objects():
        print "user:", pos_clusters.user.uname
        print "database paraphrase list:", pos_clusters.dbPara
        print "positive cluster:", pos_cluster.cluster
        print "date:", pos_cluster.date

    print

    print "---------- negative clusters ------------"
    for neg_clusters in HITClusterNegativeRes.objects():
        print "user:", neg_clusters.user.uname
        print "database paraphrase list:", neg_clusters.dbPara
        print "positive cluster:", neg_clusters.cluster
        print "date:", neg_clusters.date

# Here is the test code
if __name__ == "__main__":
    testSavedLabelRes()
