#coding=utf8
from mongoengine import *
import os
import sys

try:
    from crowdParaPhrase.settings import DBNAME
except:
    DBNAME = "crowdPara"

connect(DBNAME)

class NLPParaphrase(Document):
    ID = IntField(primary_key = True, min_value = 1)
    pname = StringField(max_length = 50)

class MatchPair(EmbeddedDocument):
    # maybe here does not need an id
    # ID = IntField(primary_key = True, min_value = 1)
    NLPParaphrase = ReferenceField(NLPParaphrase)
    confidence = FloatField()

class DatabaseParaphrase(Document):
    ID = IntField(primary_key = True, min_value = 1)
    source = StringField(max_length = 15)
    pname = StringField(max_length = 50)
    subjectExample = StringField(max_length = 50)
    objectExample = StringField(max_length = 50)


class NLPPhraseCluster(Document):
    ID = IntField(primary_key = True, min_value = 1)
    cluster = ListField(ReferenceField(NLPParaphrase))

class ParaphraseCandidate(Document):
    ID = IntField(primary_key = True, min_value = 1)
    dbPhrase = ReferenceField(DatabaseParaphrase)
    candidates = ListField(EmbeddedDocumentField(MatchPair))

class User(Document):
    ID = IntField(primary_key = True, min_value = 1)
    uname = StringField(max_length = 100)
    mail = EmailField()
    password = StringField(max_length = 100)
    confidence = FloatField()
    level = IntField()
    taskCount = IntField()

class CandDBPhrase(EmbeddedDocument):
    DatabaseParaphrase = ReferenceField(DatabaseParaphrase)
    prob = FloatField()

class HITClusterPositiveRes(Document):
    ID = IntField(primary_key = True, min_value = 1)
    user = ReferenceField(User)
    dbPara = ListField(EmbeddedDocumentField(CandDBPhrase))
    cluster = ListField(ReferenceField(NLPParaphrase))
    date = DateTimeField()

class HITClusterNegativeRes(Document):
    ID = IntField(primary_key = True, min_value = 1)
    nlp_phrase = ReferenceField(NLPParaphrase)
    user = ReferenceField(User)
    cluster = ListField(ReferenceField(NLPParaphrase))
    date = DateTimeField()

class HITMatchRes(Document):
    ID = IntField(primary_key = True, min_value = 1)
    user = ReferenceField(User)
    dbPara = ReferenceField(DatabaseParaphrase)
    clusterList = ListField(ReferenceField(HITClusterPositiveRes))
