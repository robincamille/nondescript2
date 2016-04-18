#creates bag of words array for a given text

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

def bowArray(docs):
    '''bowArray(documentList) -> creates sparse bag-of-words matrix without stopwords'''
    alltexts = []
    for doc in docs:
        alltexts.append(doc)
    vecbow = CountVectorizer(min_df=1,stop_words=None)
    bow = vecbow.fit_transform(alltexts)
    return bow

with open('top10000.txt') as vocdoc:
     voc = [w[:-1] for w in vocdoc.readlines()]

def tfidf(docs):
    '''tfidfer(documentList) -> converts collection of documents to tf*idf features matrix'''
    tfidfer = TfidfVectorizer(vocabulary=voc, \
                              min_df=1, \
                              stop_words=None, \
                              use_idf=False, \
                              smooth_idf=True)
    alltexts = []
    for doc in docs:
        alltexts.append(doc)
    tfidfcorpus = tfidfer.fit_transform(alltexts)
    return tfidfcorpus
