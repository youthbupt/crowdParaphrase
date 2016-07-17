import re

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
    while (ptr1 < len1 and ptr2 < len2):
        cmpRes = cmpPair(list1[ptr1], list2[ptr2])
        if cmpRes < 0:
            ptr1 += 1
        elif cmpRes > 0:
            ptr2 += 1
        else:
            sameCount += 1
            ptr1 += 1
            ptr2 += 1
    return (sameCount + 0.0) / max(len1, len2)

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
    with open("/media/database/dbpedia2014_sorted_dbo_qald", "r") as fin:
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
            phraseList.append((subj, obj))

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

        for p in phraseList.items():
            phraseSimi[p[0]] = sorted(p[1], cmp = lambda x, y: cmp(x[1], y[1]))
            print p[0], phraseSimi[p[0]]

if __name__ == "__main__":
    filterQALDPhrase()