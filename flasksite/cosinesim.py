#similarity between two docs
# http://stackoverflow.com/questions/8897593/similarity-between-two-text-documents

from sklearn.feature_extraction.text import TfidfVectorizer

def sim(doc1, doc2):
    documents = [doc1, doc2]
    tfidf = TfidfVectorizer().fit_transform(documents)
    pairwise_similarity = tfidf * tfidf.T
    return pairwise_similarity
