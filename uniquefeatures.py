# get word freqs, sent lengths, avg word lengths for large corpus
# then input: 7k+-word doc, output: unusual features

from nltk import FreqDist
from math import log
import nltk.data
from  more_itertools import unique_everseen as dedup
sentsplitter = nltk.data.load('tokenizers/punkt/english.pickle')
#tokenizer does not handle periods or ellipses well



def getfreq(text):
    """Returns frequency distribution of a text, from NLTK"""
    fd = FreqDist(text)
    return fd

def lowertext(text):
    """Returns a text in all lowercase"""
    lowtext = []
    for w in text:
        w = w.lower()
        lowtext.append(w) 
    return lowtext

infile = open('top10000.txt','r') #not stemmed
top10000 = infile.readlines()
infile.close()

def top10k(text): #currently top10000
    """Returns words, array of frequencies for only top 10,000 (9,989 deduped) words in English (OED)"""
    #text = text.split()
    top10kdict = {}
    for word in top10000:
        top10kdict[word[:-1]] = 0 # {'other': 0, 'take': 0, ...}
        
    for word in text:
        word = word.lower()
        if word in top10kdict:
            top10kdict[word] += 1
    top10kfreqs = []
    top10kwords = []
    for key, value in sorted(top10kdict.items()):
        top10kwords.append(key)
        top10kfreqs.append(value/float(len(text)))
    return top10kwords, top10kfreqs # [0.03731343283582089, 0.007462686567164179,...]

def top10kcounts(text): #currently top10000
    """Returns words, array of counts for only top 10,000 (9,989 deduped) words in English (OED)"""
    #text = text.split()
    top10kdict = {}
    for word in top10000:
        top10kdict[word[:-1]] = 0 # {'other': 0, 'take': 0, ...}
        
    for word in text:
        word = word.lower()
        if word in top10kdict:
            top10kdict[word] += 1
    top10kcounts = []
    top10kwords = []
    for key, value in sorted(top10kdict.items()):
        top10kwords.append(key)
        top10kcounts.append(value)
    return top10kwords, top10kcounts # [0.03731343283582089, 0.007462686567164179,...]

def avgwordlength(text):
    """Returns average word length in a text (float). Text must be a list."""
    if len(text) == 0:
        return 0.0
    else:
        words = list(dedup(text))
        totchars = len(''.join(words))
        return totchars / float(len(words))

def avgsentlength(text):
    """Returns average sentence length in a text, in chars (float). Text must be a list."""
    textstring = ' '.join(text)
    sents = sentsplitter.tokenize(textstring)
    totalsentlength = 0
    if len(sents) == 0:
        return 0
    else:
        for s in sents:
            totalsentlength = totalsentlength + len(s) #length in chars
        return totalsentlength / float(len(sents))

##filename = open('blogtrain/890034.female.23.indUnk.Scorpio43.txt','r')
##text = filename.read().split()
##filename.close()




