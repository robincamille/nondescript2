#similarity between two docs
# http://stackoverflow.com/questions/8897593/similarity-between-two-text-documents

from sklearn.feature_extraction.text import TfidfVectorizer
from numpy import dot
from math import sqrt

datadir = '/Users/robin/Documents/Thesis_local/corpora/blogs/train70_split/' #data directory
infile = open('train70.txt','r')
train70docs = infile.readlines()[:2]
infile.close()

##for doc in train70docs[:2]:
##    infile = open(datadir + doc[:-1],'r') #[:-1] = no \n
##    text = infile.read().decode('utf-8', 'ignore').split()
##    infile.close()

documents = [open(f) for f in train70docs] #first two
tfidf = TfidfVectorizer().fit_transform(documents)
pairwise_similarity = tfidf * tfidf.T
print pairwise_similarity


#http://stackoverflow.com/questions/2380394/simple-implementation-of-n-gram-tf-idf-and-cosine-similarity-in-python

inf = open('train70_freqs_smoothed.csv','r')
f = inf.readlines()[:2] #first two docs
inf.close()

u = f[0]
v = f[1]

sim = dot(u,v) / (sqrt(dot(u,u))) * (sqrt(dot(v,v)))
print sim
