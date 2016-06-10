#coding=utf8
from MongoUtils import MongoUtils
from model import ParaphraseCandidate
import random

# global parameters
candPairLen = len(ParaphraseCandidate.objects)
print "length of paraphrase candidates list: %d" % candPairLen

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
        print len(resList)
        return resList

# Here is the test code
if __name__ == "__main__":
    preSet = set()
    PhraseUtils.getRandomHIT(preSet)
