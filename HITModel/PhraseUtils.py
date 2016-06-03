#coding=utf8
from MongoUtils import MongoUtils
from model import ParaphraseCandidate

class PhraseUtils():
	candPairLen = ParaphraseCandidate.count

	@staticmethod
	def getRandomHIT(MAX_DB_PHRASE = 5, MAX_NLP_PHRASE = 20):
		NLPPhraseCount = 0
		selectedDict = dict()
		while (NLPPhraseCount < MAX_NLP_PHRASE):
			nowPhraseId = random.randint(candPairLen)
			now
			