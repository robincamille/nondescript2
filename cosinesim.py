#Outputs a similarity score between two docs.
#Dissimilar texts tend to score <0.4; very similar score >0.85.

from sklearn.feature_extraction.text import TfidfVectorizer

def sim(doc1, doc2):
    documents = [doc1, doc2]
    tfidf = TfidfVectorizer().fit_transform(documents)
    pairwise_similarity = tfidf * tfidf.T
    return pairwise_similarity
