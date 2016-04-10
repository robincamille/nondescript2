##from numpy import mean
##from nondescript import changewords
import toponly
from  more_itertools import chunked
from sklearn.naive_bayes import GaussianNB
from sklearn.externals import joblib
from random import randint
from bowmaker import bowArray, tfidf

printclassify = []
otherauths = []
comparedocs = []
comparedocspostanon = []
targets = []
authcount = 0
topnum = 10000

print "Setting up random docs for comparison"
listdir = '/Users/robin/Documents/Thesis_local/corpora/blogs/train/'
while len(otherauths) < 20: #number of authors to compare to
    with open('train_above700Kbytes.txt') as listauths:
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
        comparedocspostanon.append(toponly.top(' '.join(fulltextdocs[4]),topnum))
        comparedocspostanon.append(toponly.top(' '.join(fulltextdocs[6]),topnum))
        targets.append(authcount)
        targets.append(authcount)
        authcount += 1

#set up doc lists and targets
anontarget = targets[-1] + 1

targets.append(anontarget)
targets.append(anontarget)

with open('compare-doc.txt') as sample:
    sampletext = sample.read()
    comparedocs.append(toponly.top(sampletext,topnum))
    comparedocspostanon.append(toponly.top(sampletext,topnum))

with open('message-doc.txt') as message:
    comparedocs.append(toponly.top(message.read(),topnum))
with open('message-doc_anond.txt') as message:
    comparedocspostanon.append(toponly.top(message.read(),topnum))


with open('top10000.txt') as smoother:
    smoothertext = smoother.read()
    comparedocs.append(toponly.top(smoothertext,topnum))
    comparedocspostanon.append(toponly.top(smoothertext,topnum))
targets.append(targets[-1] + 1) #first doc has all words considered, to smooth and avoid array errors

##bow = bowArray(comparedocs).toarray()
##bowpostanon = bowArray(comparedocspostanon).toarray()

bow = tfidf(comparedocs).toarray()
bowpostanon = tfidf(comparedocspostanon).toarray()

print "Gaussian Naive Bayes Classifier"
gnb = GaussianNB()
preds = gnb.fit(bow, targets).predict(bow)
score = gnb.score(bow,targets)
printclassify.append("Overall training classifier score: " + str(score))
printclassify.append("Probability the document is yours: "+ str(gnb.predict_proba(bow)[-1][-1]))
if preds[-2] == anontarget:
    printclassify.append("Original document is classified as yours.")
else:
    printclassify.append("Original document successfully anonymous.\n")
classif = joblib.dump(gnb,'useclassifier') #save classifier
print preds

#use trained classifier on new text
gnbtest = joblib.load(classif[0]) #must have saved a classifier previously
#predstest = gnbtest.fit(bowpostanon,targets).predict(bowpostanon)
predstest = gnbtest.predict(bowpostanon)
scoretest =  gnbtest.score(bowpostanon,targets)
printclassify.append("Overall testing classifier score: " + str(scoretest))
#printclassify.append("Probability the document is yours: " + str(gnbtest.predict_proba(bowpostanon)[-1][-1]))
if predstest[-2] == anontarget:
    printclassify.append("Anonymized document is still classified as yours.")
else:
    printclassify.append("Anonymized document successfully anonymized.")
print predstest


for i in printclassify:
    print i

