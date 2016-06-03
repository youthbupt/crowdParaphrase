#coding=utf8
from mongoengine import *
import os
import sys

try:
	from crowdParaPhrase.settings import DBNAME
except:
	DBNAME = "crowdParaHIT"

connect(DBNAME)

class NLPParaphrase(Document):
	pname = StringField(primary_key = True, max_length = 50)

class MatchPair(EmbeddedDocument):
	NLPParaphrase = ReferenceField(NLPParaphrase)
	confidence = DecimalField()

class DatabaseParaphrase(Document):
	source = StringField(max_length = 15)
	pname = StringField(primary_key = True, max_length = 50)

class ParaphraseCandidate(Document):
	ID = IntField(min_value = 1)
	DbpediaParaphrase = ReferenceField(DatabaseParaphrase)
	candidates = ListField(EmbeddedDocumentField(MatchPair))

class User(Document):
	uname = StringField(primary_key = True, max_length = 100)
	confidence = DecimalField()
	level = IntField()
	taskCount = IntField()

class HITClusterRes(Document):
	user = ReferenceField(User)
	posRes = ListField(ReferenceField(NLPParaphrase))
	negRes = ListField(ReferenceField(NLPParaphrase))
	date = DateTimeField()

class HITMatchRes(Document):
	user = ReferenceField(User)
	dbPara = ReferenceField(DatabaseParaphrase)
	cluster = ListField(EmbeddedDocumentField(MatchPair))
	conf = DecimalField()
