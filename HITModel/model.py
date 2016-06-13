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
    ID = IntField(primary_key = True, min_value = 1)
    pname = StringField(max_length = 50)

class MatchPair(EmbeddedDocument):
    # maybe here does not need an id
    # ID = IntField(primary_key = True, min_value = 1)
    NLPParaphrase = ReferenceField(NLPParaphrase)
    confidence = DecimalField()

class DatabaseParaphrase(Document):
    ID = IntField(primary_key = True, min_value = 1)
    source = StringField(max_length = 15)
    pname = StringField(max_length = 50)

class ParaphraseCandidate(Document):
    ID = IntField(primary_key = True, min_value = 1)
    DbpediaParaphrase = ReferenceField(DatabaseParaphrase)
    candidates = ListField(EmbeddedDocumentField(MatchPair))

class User(Document):
    ID = IntField(primary_key = True, min_value = 1)
    uname = StringField(max_length = 100)
    confidence = DecimalField()
    level = IntField()
    taskCount = IntField()

class HITClusterPositiveRes(Document):
    ID = IntField(primary_key = True, min_value = 1)
    user = ReferenceField(User)
    dbPara = ListField(IntField)
    cluster = ListField(IntField)
    date = DateTimeField()

class HITClusterNegativeRes(Document):
    ID = IntField(primary_key = True, min_value = 1)
    nlp_phrase = IntField()
    user = ReferenceField(User)
    cluster = ListField(IntField)
    date = DateTimeField()

class HITMatchRes(Document):
    ID = IntField(primary_key = True, min_value = 1)
    user = ReferenceField(User)
    dbPara = ReferenceField(DatabaseParaphrase)
    cluster = ListField(EmbeddedDocumentField(MatchPair))
    conf = DecimalField()
