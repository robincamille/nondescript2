#similarity between two docs
# http://stackoverflow.com/questions/8897593/similarity-between-two-text-documents

from sklearn.feature_extraction.text import TfidfVectorizer
#from numpy import dot, array
#from math import sqrt

##doc1f = open('testdoc1a.txt','r')
##doc1 = doc1f.read()
##doc1f.close()
##
##doc2f = open('testdoc1b_nondescripted.txt','r')
##doc2 = doc2f.read()
##doc2f.close()

#datadir = '/Users/robin/Documents/Thesis_local/corpora/blogs/train70_split/' #data directory
#infile = open('train70.txt','r')
#infile.close()

##for doc in train70docs[:2]:
##    infile = open(datadir + doc[:-1],'r') #[:-1] = no \n
##    text = infile.read().decode('utf-8', 'ignore').split()
##    infile.close()

##train70docs = ['/Users/robin/Documents/Thesis_local/corpora/blogs/train70_split/1752515.female.27.Science.Aries28.txt',\
##'/Users/robin/Documents/Thesis_local/corpora/blogs/train70_split/1752515.female.27.Science.Aries29.txt']
##
##documentsfiles = [open(f) for f in train70docs] #first two
##documents = [f.read() for f in documentsfiles] #first two

def main(doc1, doc2):
    documents = [doc1, doc2]
    tfidf = TfidfVectorizer().fit_transform(documents)
    pairwise_similarity = tfidf * tfidf.T
    return pairwise_similarity


#http://stackoverflow.com/questions/2380394/simple-implementation-of-n-gram-tf-idf-and-cosine-similarity-in-python

##inf = open('train70_freqs_2_smoothed.csv','r')
##f = inf.readlines()[202:204] #first two docs
##inf.close()
##
##uraw = f[0]
##ul = uraw.split(',')[:-1] #ignore line ending
##u = []
##for i in ul:
##    u.append(float(i)) #make strings into floats
##u = array(u) #make into numpy 1D array (9989 x 1)
##
##vraw = f[1]
##vl = vraw.split(',')[:-1]
##v = []
##for i in vl:
##    v.append(float(i))
##v = array(v)
##
##sim = dot(u,v) / (sqrt(dot(u,u))) * (sqrt(dot(v,v)))
##print sim
##
