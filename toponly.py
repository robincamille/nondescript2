# considers only the words in the top 9,989,
# 1000, or 100 most frequently used words in
# the corpus.

from sources import *
import re

with open(topcorpuswords10000) as top10kfile:
    top10kraw = top10kfile.readlines()
    top10k = [i[:-1] for i in top10kraw]

with open(topcorpuswords5000) as top5kfile:
    top5kraw = top5kfile.readlines()
    top5k = [i[:-1] for i in top5kraw]

with open(topcorpuswords1000) as top1kfile:
    top1kraw = top1kfile.readlines()
    top1k = [i[:-1] for i in top1kraw]

with open(topcorpuswords100) as top100file:
    top100raw = top100file.readlines()
    top100 = [i[:-1] for i in top100raw]

def top(fulltext, howmany = None):
    """Returns a given text with only the words in the top 100, 1000, or 10,000 words in English, or all words (default)."""
    if howmany == 10000:
        top = [w for w in fulltext.lower().split() if w in top10k]
        return ' '.join(top)
    if howmany == 5000:
        #top = [w for w in fulltext.lower().split() if w in top1k]
        top = []
        fulltext = re.findall(r"[\w']+|[!\"#$%&()*+,-./:;<=>?@\[\]^_`{|}~]",fulltext.lower())
        for w in fulltext:
            if w in top5k:
                top.append(w)
        returntext = ' '.join(top)
        return returntext
    if howmany == 1000:
        #top = [w for w in fulltext.lower().split() if w in top1k]
        top = []
        fulltext = re.findall(r"[\w']+|[!\"#$%&()*+,-./:;<=>?@\[\]^_`{|}~]",fulltext.lower())
        for w in fulltext:
            if w in top1k:
                top.append(w)
        returntext = ' '.join(top)
        #print(returntext[:50]) #my message word , email , , , , every year , i < blog > < date > , july ,
        return returntext
    if howmany == 100:
        top = [w for w in fulltext.lower().split() if w in top100]
        return ' '.join(top)
    if howmany == None:
        return fulltext

