#coding = utf8
import re
import json
import sys
sys.path.append("../HITModel")
from PhraseUtils import PhraseUtils


def getTuple(s):
    prefix = "<http://dbpedia.org/resource/"
    idx = s.find(prefix)
    if idx == 0:
        return s[len(prefix): -1].strip()
    prefix = "<http://dbpedia.org/ontology/"
    idx = s.find(prefix)
    if idx == 0:
        return s[len(prefix): -1].strip()

def cmpPair(p1, p2):
    if p1[0] != p2[0]:
        return cmp(p1[0], p2[0])
    return cmp(p1[1], p2[1])

def jaccardPhraseSimi(list1, list2):
    len1 = len(list1)
    len2 = len(list2)
    ptr1 = 0
    ptr2 = 0
    sameCount = 0
    totalCount = 0
    while (ptr1 < len1 and ptr2 < len2):
        cmpRes = cmpPair(list1[ptr1], list2[ptr2])
        if cmpRes < 0:
            ptr1 += 1
            totalCount += 1
        elif cmpRes > 0:
            ptr2 += 1
            totalCount += 1
        else:
            sameCount += 1
            totalCount += 1
            ptr1 += 1
            ptr2 += 1
    return (sameCount + 0.0) / totalCount

def filterQALDPhrase():
    QALDPhraseDict = set()
    with open("/media/database/dbpedia_DKRL_7.txt") as fin:
        lines = re.split(r"[\r\n]", fin.read())
        for line in lines:
            if len(line) < 5: continue
            tup = line.split("\t")
            if len(tup) != 3: continue
            subj = getTuple(tup[0])
            relation = getTuple(tup[1])
            obj = getTuple(tup[2])
            QALDPhraseDict.add(relation)

    with open("/media/database/dbpedia2014_sorted_dbo", "r") as fin, \
    open("/media/database/dbpedia2014_sorted_dbo_qald", "w") as fout:
        lines = re.split(r"[\r\n]", fin.read())
        # phraseList = {}
        cntPhrase = 0
        for line in lines:
            if len(line) < 10: continue
            tup = line.split('\t')
            if len(tup) != 3: continue
            relation = getTuple(tup[1])
            if relation not in QALDPhraseDict:
                continue
            cntPhrase += 1
            if cntPhrase % 100 == 0:
                print "Dealed with %d QALD tuples!" % cntPhrase
            fout.write(line + "\n")

def minSimilarDBPhrase():
    with open("/media/database/dbpedia2014_sorted_dbo_qald", "r") as fin, \
    open("../data/similar_qald_phrase.txt", "w") as fout:
        lines = re.split(r"[\r\n]", fin.read())
        phraseList = {}
        for line in lines:
            if len(line) < 10: continue
            tup = line.split('\t')
            if len(tup) != 3: continue
            relation = getTuple(tup[1])
            subj = getTuple(tup[0])
            obj = getTuple(tup[2])
            if relation not in phraseList:
                phraseList[relation] = []
            phraseList[relation].append((subj, obj))

        for phrase, entityList in phraseList.items():
            phraseList[phrase] = sorted(entityList, cmpPair)

        phrase = phraseList.keys()
        phraseCount = len(phraseList)
        phraseSimi = {}

        for p in phrase:
            phraseSimi[p] = {}

        for i in xrange(phraseCount):
            phrase1 = phrase[i]
            for j in xrange(i + 1, phraseCount):
                phrase2 = phrase[j]
                simi = jaccardPhraseSimi(phraseList[phrase1], phraseList[phrase2])
                phraseSimi[phrase1][phrase2] = simi
                phraseSimi[phrase2][phrase1] = simi

        for p in phraseSimi.items():
            phraseSimi[p[0]] = sorted(p[1].items(), cmp = lambda x, y: cmp(y[1], x[1]))
            print p[0], phraseSimi[p[0]]
            fout.write(p[0] + "\t" + json.dumps(phraseSimi[p[0]]) + "\n")

def displaySimilarPhrase(topk = 5):
    with open("../data/similar_qald_phrase.txt", "r") as fin:
        lines = re.split(r"[\r\n]", fin.read())
        for line in lines:
            if len(line) < 10: continue
            tup = line.split('\t')
            if len(tup) != 2: continue
            simiPair = json.loads(tup[1])
            simiPair = filter(lambda x: x[1] > 0, simiPair)[:topk]
            print tup[0], simiPair

def insertPhraseToMongo(topk = 5):
    with open("../data/similar_qald_phrase.txt", "r") as fin:
        lines = re.split(r"[\r\n]", fin.read())
        dbphrase = {}
        for line in lines:
            if len(line) < 10: continue
            tup = line.split('\t')
            if len(tup) != 2: continue
            if tup[0] not in dbphrase:
                tmp_phrase = PhraseUtils.getDBPhraseByName(tup[0])
                if tmp_phrase == None:
                    print "%s not exist in database" % simi[0]
                    continue
                dbphrase[tup[0]] = tmp_phrase
            now_phrase = dbphrase[tup[0]]
            simi_phrase = []
            simiPair = json.loads(tup[1])
            simiPair = filter(lambda x: x[1] > 0, simiPair)[:topk]
            for simi in simiPair:
                if simi[0] not in dbphrase:
                    tmp_phrase = PhraseUtils.getDBPhraseByName(simi[0])
                    if tmp_phrase == None:
                        print "%s not exist in database" % simi[0]
                        continue
                    dbphrase[simi[0]] = tmp_phrase

                simi_phrase.append(dbphrase[simi[0]])
            
            #now_phrase.similarPhrase = simi_phrase
            now_phrase.update(similarPhrase = simi_phrase)
            print simi_phrase, now_phrase.similarPhrase
            #now_phrase.update()

            print tup[0], simiPair

def showSimiPhrase():
    phrase_list = PhraseUtils.getAllDBPhrase()
    for phrase in phrase_list:
        print phrase
        print phrase.similarPhrase

if __name__ == "__main__":
    #displaySimilarPhrase()
    # showSimiPhrase()
    # insertPhraseToMongo()
    showSimiPhrase()
