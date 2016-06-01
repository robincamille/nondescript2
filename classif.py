# Creates term-frequency array for a given text.
# Note that this is tf, not tf*idf.

from sklearn.feature_extraction.text import TfidfVectorizer
from sources import topcorpuswords1000

# Use only vocabulary of top 10,000 most frequent words in corpus
# (out of the box, these scripts only consider the top 1,000,
# but you can change that number in the classifactory.classifydocs(...) function)
with open(topcorpuswords1000) as vocdoc:
     voc = [w[:-1] for w in vocdoc.readlines()]

def tfidf(docs):
    '''tfidfer(documentList) -> converts collection of documents to tf matrix'''
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
