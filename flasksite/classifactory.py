#Uses a Gaussian Naive Bayes classifier on a set of documents converted to tf*idf array.
#Background corpus: 4 documents each from 10 known authors from given directory.
#Trains classifier on known documents (20 background, author sample, author original message).
#Then runs trained classifier on new documents to predict authors (20 background,
#author sample, new message). 
#Returns textual description of testing classifier results.

import toponly
from  more_itertools import chunked
from sklearn.naive_bayes import GaussianNB
from sklearn.externals import joblib
from random import randint
from classif import tfidf

def classifydocs(listdir, authsfile, sampletext, messagetext, topnum = None):
    """Naive Bayes classifier returns classification for a given document,
    compared to another document by the same author, and 2 documents each from 5
    randomly chosen authors in the given directory. tf*idf arrays created for (topnum)
    characters: 100, 1000, 10000 of the most common English words, or all words (default)."""
    printclassify = []
    otherauths = []
    comparedocs = []
    comparedocstest = []
    targets = []
    authcount = 0
    #topnum = 10000

##    print "Setting up random docs for comparison"
##    listdir = '/Users/robin/Documents/Thesis_local/corpora/blogs/train/'
    while len(otherauths) < 5: #number of authors to compare to
        with open(authsfile) as listauths:
            allauths = listauths.readlines()
            auth = allauths[randint(0,len(allauths)-1)]
            if auth[:-1] in otherauths:
                pass
            else:
                otherauths.append(auth[:-1])

    for a in otherauths:
        with open(listdir + a) as fulltext:
            fulltext = fulltext.read().split()
            fulltextdocs = chunked(fulltext,7000)
            fulltextdocs = list(fulltextdocs)
            comparedocs.append(toponly.top(' '.join(fulltextdocs[0]),topnum))
            comparedocs.append(toponly.top(' '.join(fulltextdocs[2]),topnum))
            comparedocstest.append(toponly.top(' '.join(fulltextdocs[4]),topnum))
            comparedocstest.append(toponly.top(' '.join(fulltextdocs[6]),topnum))
            targets.append(authcount)
            targets.append(authcount)
            authcount += 1

    #set up doc lists and targets
    anontarget = targets[-1] + 1

    targets.append(anontarget)
#    targets.append(anontarget)

    comparedocs.append(toponly.top(sampletext,topnum))
    #comparedocstest.append(toponly.top(sampletext,topnum))
    
    #comparedocs.append(toponly.top(messagetextorig,topnum))
    comparedocstest.append(toponly.top(messagetext,topnum))

    

##    with open('compare-doc.txt') as sample:
##        sampletext = sample.read()
##        comparedocs.append(toponly.top(sampletext,topnum))
##        comparedocstest.append(toponly.top(sampletext,topnum))
##
##    with open('message-doc.txt') as message:
##        comparedocs.append(toponly.top(message.read(),topnum))
##    with open('message-doc_anond.txt') as message:
##        comparedocstest.append(toponly.top(message.read(),topnum))


    with open('top10000.txt') as smoother:
        smoothertext = smoother.read()
        comparedocs.append(toponly.top(smoothertext,topnum))
        comparedocstest.append(toponly.top(smoothertext,topnum))
    targets.append(targets[-1] + 1) #first doc has all words considered, to smooth and avoid array errors

    tfarray = tfidf(comparedocs).toarray()
    tfarraynew = tfidf(comparedocstest).toarray()

##    print "Gaussian Naive Bayes Classifier"
    gnb = GaussianNB()
    preds = gnb.fit(tfarray, targets).predict(tfarray)
##        score = gnb.score(tfarray,targets)
##        printclassify.append("Overall training classifier score: " + str(score))
##        printclassify.append("Probability the original message is yours: "+ str(gnb.predict_proba(tfarray)[-1][-1]))
##    if preds[-2] == anontarget:
##        printclassify.append("Original document is classified as yours.")
##    else:
##        printclassify.append("Original document successfully anonymous.\n")
    classif = joblib.dump(gnb,'useclassifier') #save classifier
    printclassify.append(preds)

    #use trained classifier on new text
    gnbtest = joblib.load(classif[0]) #must have saved a classifier previously
    #predstest = gnbtest.fit(tfarraynew,targets).predict(tfarraynew)
    predstest = gnbtest.predict(tfarraynew)
    scoretest =  gnbtest.score(tfarraynew,targets)
    ##printclassify.append("Probability the provided message is yours: " + str(gnbtest.predict_proba(tfarraynew)[-1][-1]))
    if predstest[-2] == anontarget:
        printclassify.append("Provided document is still classified as yours.")
    else:
        printclassify.append("Provided document successfully anonymized for this classifier.")
    printclassify.append("Overall (testing) classifier score: " + str(scoretest))
    printclassify.append(predstest)

    return printclassify


print '100-----------------------'
for i in classifydocs('/Users/robin/Documents/Thesis_local/corpora/blogs/train/',\
                                             'train_above700Kbytes.txt',\
                                             'compare-doc.txt',\
                                             'message-doc_not.txt',\
                                             100):
    print i
print '1000-----------------------'
for i in classifydocs('/Users/robin/Documents/Thesis_local/corpora/blogs/train/',\
                                             'train_above700Kbytes.txt',\
                                             'compare-doc.txt',\
                                             'message-doc_not.txt',\
                                             1000):
    print i
print '1000-----------------------'
for i in classifydocs('/Users/robin/Documents/Thesis_local/corpora/blogs/train/',\
                                             'train_above700Kbytes.txt',\
                                             'compare-doc.txt',\
                                             'message-doc_not.txt',\
                                             1000):
    print i

