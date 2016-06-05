#coding=utf8
from MongoUtils import MongoUtils
from model import ParaphraseCandidate
import random

# global parameters
candPairLen = len(ParaphraseCandidate.objects)

class PhraseUtils():

	@staticmethod
	def getRandomHIT(MAX_DB_PHRASE = 5, MAX_NLP_PHRASE = 20):
		NLPPhraseCount = 0
		selectedDict = dict()
		
		while (NLPPhraseCount < MAX_NLP_PHRASE):
			if len(selectedDict) == candPairLen:
				break
			nowCandId = random.randint(0, candPairLen)
			if nowCandId in selectedDict:
				continue
			nowCandList = ParaphraseCandidate.objects(ID = nowCandId)
			if nowCandList is None or len(nowCandList) == 0:
				continue
			nowCand = nowCandList[0]
			selectedDict[nowCandId] = []
			candLen = len(nowCand.candidates)
			if (NLPPhraseCount + candLen <= MAX_NLP_PHRASE):
				for nlp_phrase in nowCand.candidates:
					selectedDict[nowCandId].append(nlp_phrase)
					print nlp_phrase
				MAX_NLP_PHRASE += candLen
			else:
				cand = []
				for nlp_phrase in nowCand.candidates:
					cand.append(nlp_phrase)
				random.shuffle(cand)
				i = 0
				while NLPPhraseCount < MAX_NLP_PHRASE:
					selectedDict[nowCandId].append(cand[i])
					i += 1
					NLPPhraseCount += 1
			print selectedDict[nowCandId]
		resList = []
		for db_id, cand_list in selectedDict.items():
			for cand in cand_list:
				resList.append(db_id, cand.)
		print selectedDict


# Here is the test code
if __name__ == "__main__":
	PhraseUtils.getRandomHIT()
			