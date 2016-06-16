#coding=utf8
from MongoUtils import MongoUtils
from model import ParaphraseCandidate, NLPParaphrase, HITClusterPositiveRes, \
HITClusterNegativeRes, User, CandDBPhrase, DatabaseParaphrase
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
    def getDBPhrase(phraseId):
        phrase = DatabaseParaphrase.objects(ID = phraseId)
        if len(phrase) == 0:
            return None
        return phrase[0]

    @staticmethod
    def insertLabeledRes(user, cluster_list):
        nlpParaDict = {}
        dbParaDict = {}
        posIdList = []
        for cluster in cluster_list:
            nowCluster = []
            dbParaCount = {}
            clusterLen = len(cluster)
            for nlpId, dbId in cluster:
                nlpId = int(nlpId)
                dbId = int(dbId)
                if nlpId not in nlpParaDict:
                    nlpParaDict[nlpId] = PhraseUtils.getNLPPhrase(nlpId)
                if dbId not in dbParaDict:
                    dbParaDict[dbId] = PhraseUtils.getDBPhrase(dbId)
                if nlpParaDict[nlpId] is None or dbParaDict[dbId] is None:
                    continue
                if nlpId is not None:
                    nowCluster.append(nlpParaDict[nlpId])
                if dbId not in dbParaCount:
                    dbParaCount[dbId] = 1.0 / clusterLen
                else:
                    dbParaCount[dbId] += 1.0 / clusterLen
            # dbParaList = dbParaCount.items()
            dbPara = []
            for dbId, prob in dbParaCount.items():
                # print dbId, prob
                if dbId in dbParaDict and dbParaDict[dbId] is not None:
                    dbPara.append(CandDBPhrase(DatabaseParaphrase = dbParaDict[dbId], prob = prob))
            if len(nowCluster) < 1 or len(dbPara) < 1:
                continue

            posId = len(HITClusterPositiveRes.objects()) + 1
            posIdList.append(posId)
            posObj = HITClusterPositiveRes(ID = posId, user = user, \
                dbPara = dbPara, cluster = nowCluster, date = datetime.now())
            posObj.save()

        l = len(cluster_list)
        if l == 0: return
        for x in xrange(l):
            cluster = cluster_list[x]
            for nlpId, dbId in cluster:
                # print nlpId
                if nlpId not in nlpParaDict:
                    continue
                nlpObj = nlpParaDict[nlpId]
                if nlpObj is None:
                    continue
                negPhrase = []
                for y in xrange(l):
                    if x == y:
                        continue
                    neg_cluster = cluster_list[y]
                    for negNlp, db in neg_cluster:
                        if negNlp in nlpParaDict and nlpParaDict[negNlp] is not None:
                            negPhrase.append(nlpParaDict[negNlp])
                if len(negPhrase) > 0:
                    negObj = HITClusterNegativeRes(ID = len(HITClusterNegativeRes.objects()) + 1, \
                        nlp_phrase = nlpObj, user = user, cluster = negPhrase, date = datetime.now())
                    negObj.save()
        return posIdList

    @staticmethod
    def getPosCluster(clusterId):
        clusters = HITClusterPositiveRes.objects(ID = clusterId)
        if len(clusters) > 0:
            return clusters[0]
        return None

    @staticmethod
    def getMatchHIT(clusterList, EACH_CLUSTER_SHOWN_COUNT = 3):
        posCluster = []
        dbParaList = []
        dbParaSet = set()
        for cid in clusterList:
            cluster = PhraseUtils.getPosCluster(cid)
            if cluster is not None:
                
                nlpParaList = []
                for dbPara in cluster.dbPara:
                    if dbPara.DatabaseParaphrase.ID not in dbParaSet:
                        dbParaSet.add(dbPara.DatabaseParaphrase.ID)
                        dbParaDict = {}
                        dbParaDict["dbId"] = dbPara.DatabaseParaphrase.ID
                        dbParaDict["dbParaName"] = dbPara.DatabaseParaphrase.pname
                        dbParaList.append(dbParaDict)
                nowCluster = []
                for nlpPara in cluster.cluster:
                    if len(nlpParaList) >= EACH_CLUSTER_SHOWN_COUNT:
                        break
                    """
                    nlpParaDict = {}
                    nlpParaDict["nlpId"] = nlpPara.ID
                    nlpParaDict["nlpName"] = nlpPara.pname
                    # nlpParaList.append(nlpPara.ID)
                    nowCluster.append(nlpParaDict)
                    """
                    nowCluster.append(nlpPara.pname)
                # random.shuffle(nlpParaList)
                # posCluster.append((cid, nlpParaList[:EACH_CLUSTER_SHOWN_COUNT]))
                posCluster.append((cid, nowCluster))
        print "----------------database paraphrases----------------"
        print dbParaList
        print "-----------------positive clusters-----------------"
        print posCluster
        return dbParaList, posCluster


    @staticmethod
    def cleanLabeledRes():
        HITClusterPositiveRes.objects().delete()
        HITClusterNegativeRes.objects().delete()

def testGetRandomHIT():
    preSet = set()
    res = PhraseUtils.getRandomHIT(preSet)
    print res

def printSavedLabelRes():
    print "---------- positive clusters ------------"
    for pos_cluster in HITClusterPositiveRes.objects():
        print "user:", pos_cluster.user.uname
        print "database paraphrase list:", pos_cluster.dbPara
        print "positive cluster:", pos_cluster.cluster
        print "date:", pos_cluster.date

    print

    print "---------- negative clusters ------------"
    for neg_clusters in HITClusterNegativeRes.objects():
        print "user:", neg_clusters.user.uname
        print "nlp paraphrase:", neg_clusters.nlp_phrase
        print "negative cluster:", neg_clusters.cluster
        print "date:", neg_clusters.date

def testInsertLabeledRes():
    print "test lalbel results inserting function"
    user = User.objects(uname = "ys")[0]
    cluster_list = [[[29129,134]],[[29096,134]],[[29130,134]],[[29109,134]],[[29121,134]],[[29100,134]],\
    [[29108,134]],[[29099,134]],[[29116,134]],[[29112,134]],[[29092,134]],[[29143,134]],[[29119,134]],\
    [[29111,134],[29101,134],[29118,134],[29125,134],[29136,134],[29137,134]],[[29097,134]]]

    PhraseUtils.insertLabeledRes(user, cluster_list)

def testMatchHITs():
    print "Test matching from nlp paraphrase to database paraphrase"
    clusters = [89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103]
    PhraseUtils.getMatchHIT(clusters)

# Here is the test code
if __name__ == "__main__":
    # PhraseUtils.cleanLabeledRes()
    # testInsertLabeledRes()
    # printSavedLabelRes()
    testMatchHITs()
