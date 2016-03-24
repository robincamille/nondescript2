#!/usr/bin/env python
# -*- coding: utf-8 -*-

##Robin Camille Davis
##March 2015
##NLP, ML, and the Web (Rosenberg)
##
##Program description:
##    Trains a classifier on a set of Craigslist HTML documents
##Program input:
##    hw1_train.py [test label file] [data directory] [filename for generated classifier] [optional flags]

import re, time, datetime, sys
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import GaussianNB
from sklearn.externals import joblib  
from sklearn import tree

doclist = []        #list of document names
documents = []      #(filename, category)
allwords = []       #list of all the words
traintargets = []   #list of targets, in order of doclist and alltexts

labelfile = open(sys.argv[1],'r') #labels
labels = labelfile.readlines()
labelfile.close()

timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S')
datadir = sys.argv[2] #data directory

classifiername = 'classifier_' + sys.argv[3] + '_' + timestamp
#saves as .npy file

for line in labels: #prep documents list for classifier
    line = line.split(',')
    documents.append((line[0],line[1][:-1])) #(filename,category)
    traintargets.append(line[1][:-1])

def preptext(docname):
    '''preptext(documentName) -> opens file, scrapes just post body content, strips HTML'''
    features = []
    doclist.append(docname) #add 
    infile = open(datadir + '/' + docname,'r')
    text = infile.read()
    infile.close()
    for word in text:
        allwords.append(word)
    return text


def bowArray(docs):
    '''bowArray(documentList) -> creates sparse bag-of-words matrix without stopwords'''
    alltexts = []
    for doc in docs:
        alltexts.append(preptext(doc[0]))
    vecbow = CountVectorizer(min_df=1,stop_words=None)
    bow = vecbow.fit_transform(alltexts)
    return bow


def bigramArray(docs): 
    '''bigramArray(documentList) -> creates sparse bigram matrix without stopwords'''
    alltexts = []
    for doc in docs:
        alltexts.append(preptext(doc[0]))
    vecbig = CountVectorizer(min_df=1,stop_words=None,ngram_range=(2,2))
    biarray = vecbig.fit_transform(alltexts)
    return biarray


def tfidf(docs):
    '''tfidfer(documentList) -> converts collection of documents to tf*idf features matrix'''
    tfidfer = TfidfVectorizer(min_df=2,stop_words=None,smooth_idf=True)
    alltexts = []
    for doc in docs:
        alltexts.append(preptext(doc[0]))
    tfidfcorpus = tfidfer.fit_transform(alltexts)
    return tfidfcorpus


def dtree(data,targets,docnames):
    '''detree(data,targets,docnames) -> outputs score'''
    tr = tree.DecisionTreeClassifier()
    preds = tr.fit(data,targets).predict(data)
    print 'Number of mislabeled points out of a total %d points : %d' \
          % (data.shape[0],(targets != preds).sum())
    score = 'Score: %f' % tr.score(data,targets)
    print score
    outputfile(preds,targets,docnames)
    joblib.dump(tr,classifiername) #save classifier


def gaussNB(data,targets,docnames): 
    '''gaussNB(dataset,targets,documentNames) -> mean accuracy + output prediction file'''
    gnb = GaussianNB()
    preds = gnb.fit(data, targets).predict(data)
    print 'Number of mislabeled points out of a total %d points : %d' \
          % (data.shape[0],(targets != preds).sum())
    score = 'Score: %f' % gnb.score(data,targets)
    print score
    outputfile(preds,targets,docnames)
    joblib.dump(gnb,classifiername) #save classifier


def outputfile(preds,targets,docnames):
    outfilename = 'classifier-output_' + timestamp + '.csv'
    outfile = open(outfilename,'w')
    for i in range(len(preds)):
        #output file line: 4892794274.html,event,missed,-
        line = docnames[i] + ',' + targets[i] + ',' + preds[i]
        outfile.write(line)
        if targets[i] == preds[i]:
            outfile.write(',+\n')
        else:
            outfile.write(',-\n')
    outfile.close
    print 'Output CSV created as', outfilename


def main():
    if len(sys.argv) < 5:
        print '\nTerm vector + Gaussian Naive Bayes classifier'
        bow = bowArray(documents).toarray()
        gaussNB(bow,traintargets,doclist)
        print 'Classifier saved as as', classifiername
    elif sys.argv[4] == '-B':
        print '\nBigrams + Gaussian Naive Bayes classifier'
        big = bigramArray(documents).toarray()
        gaussNB(big,traintargets,doclist)
        print 'Classifier saved as as', classifiername
    elif sys.argv[4] == '-t':
        print '\nTf*idf + Gaussian Naive Bayes classifier'
        weights = tfidf(documents).toarray()
        gaussNB(weights,traintargets,doclist)
        print 'Classifier saved as as', classifiername
    elif sys.argv[4] == '-d':
        print '\nBag of words + Decision Tree classifier'
        bow = bowArray(documents).toarray()
        dtree(bow,traintargets,doclist)
        print 'Classifier saved as as', classifiername
    else:
        print 'Error: run command as:\nhw1_train.py [test label file] [data directory] \
[filename for generated classifier] [optional flags]'
        
        
main()


