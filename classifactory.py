# Uses a Gaussian Naive Bayes classifier on a set of documents
# converted to tf (term frequency) arrays. Trains classifier on known documents
# Then runs trained classifier on a set of new documents to predict authors.
# Returns textual description of testing classifier results as a list.
# Background corpus: 1 long document each from n known authors from given directory.

# Training document set: 2 documents each from n randomly-chosen authors, two
# parts of the user's submitted writing sample.
# Testing document set: 2 more documents each from the same 7 authors,
# the rest of the submitted writing sample, message user wishes to test for
# anonymity.


import toponly, datetime, time, re
from  more_itertools import chunked
from sklearn.naive_bayes import GaussianNB
from sklearn.externals import joblib
from random import randint
from classif import tfidf

timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('_%Y-%m-%d_%H-%M-%S')

def classifydocs(listdir, authsfile, sampletext, messagetext, topnum = 999):
    """Naive Bayes classifier returns classification for a given document,
    compared to another document by the same author, and 2 documents each from 7
    randomly chosen authors in the given directory. tf arrays created for (topnum)
    characters: 100, 1000, 10000 of the most common English words."""
    printclassify = []
    otherauths = []
    comparedocs = []
    comparedocstest = []
    targets = []
    authcount = 0

    # Choose other random authors from the background corpus
    while len(otherauths) < 5: #number of authors to compare to
        with open(authsfile, 'rb') as listauths:
            allauths = listauths.readlines()
            auth = allauths[randint(0,len(allauths)-1)]
            if auth[:-1] in otherauths:
                pass
            else:
                otherauths.append(auth[:-1])

    # Each author has one long document of at least 50,000 words
    # Split this into 7,000-word non-consec chunks
    for a in otherauths:
        with open(listdir + a, 'rb') as fulltext:
            fulltext = fulltext.read().split()
            #fulltext = re.findall(r"[\w']+|[!\"#$%&\()*+,-./:;<=>?@\[\\\]^_`{|}~]",fulltext) #error:TypeError: expected string or bytes-like object
            fulltextdocs = chunked(fulltext,7000)
            fulltextdocs = list(fulltextdocs)
            comparedocs.append(toponly.top(' '.join(fulltextdocs[0]),topnum))
            comparedocs.append(toponly.top(' '.join(fulltextdocs[2]),topnum))
            comparedocstest.append(toponly.top(' '.join(fulltextdocs[4]),topnum))
            comparedocstest.append(toponly.top(' '.join(fulltextdocs[6]),topnum))
            targets.append(authcount) # Set up targets list [0,0,1,1,...]
            targets.append(authcount)
            authcount += 1

    # Add user to end of targets list [0,0,...n,n] where author is n
    anontarget = targets[-1] + 1

    targets.append(anontarget)
    targets.append(anontarget)

    # Add submitted documents to the training and testing mini-corpora
    # Sample text is split into 3 chunks; 2 > train, 1 > test
    # Message text is added to test
    sampletext= sampletext.split()
    #sampletext = re.findall(r"[\w']+|[!\"#$%&\()*+,-./:;<=>?@\[\\\]^_`{|}~]",sampletext)
    sampletext = chunked(sampletext, (len(sampletext) / 3)) 
    sampletext = list(sampletext)
    
    comparedocs.append(toponly.top(' '.join(sampletext[0]),topnum))
    comparedocs.append(toponly.top(' '.join(sampletext[1]),topnum))

    comparedocstest.append(toponly.top(' '.join(sampletext[2]),topnum))
    comparedocstest.append(toponly.top(messagetext,topnum))

    # Set up term frequency arrays for train and test document sets
    tfarraytrain = tfidf(comparedocs).toarray()
    tfarraytest = tfidf(comparedocstest).toarray()

    # Set up classifier 
    gnb = GaussianNB()
    preds = gnb.fit(tfarraytrain, targets).predict(tfarraytrain)
    scoretrain = (gnb.score(tfarraytrain,targets)) * 100 # Testing score
    scoretrain =  "{:.1f}".format(scoretrain)
    print "Training predictions\t" + str(preds) + "\t(user is last 2 targets)\tScore: " + str(scoretrain) # To console only
    classifiername = 'classifier' #+ timestamp
    classif = joblib.dump(gnb,classifiername) #save classifier

    # Test trained classifier on new text, return score and message-specific report
    gnbtest = joblib.load(classif[0]) #must have saved a classifier previously
    predstest = gnbtest.predict(tfarraytest)
    scoretest = (gnbtest.score(tfarraytest,targets)) * 100 # Testing score
    scoretest =  "{:.1f}".format(scoretest)
    print "Testing predictions\t" + str(predstest) + "\t(user is last 2 targets)\tScore: " + str(scoretest)  # To console only
    if predstest[-1] == anontarget:
        printclassify.append("Try again: Message is still attributed to you by this classifier.")
    else:
        printclassify.append("Success: Message successfully anonymized for this classifier.")
    printclassify.append("Overall classifier score: " + str(scoretest) + ' out of 100')

    return printclassify
