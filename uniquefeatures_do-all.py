# train 70 corpus word counts, word freqs, word lengths, sent lengths
# outputs 4 docs

#10k words from google ngrams = 9989 deduped :S 

import uniquefeatures as uf

outfreq = open('train70long_freqs_2.csv','w')
outcount = open('train70long_counts_2.csv','w')
totcount = open('train70long_all-counts_2.csv','w')
outword = open('train70long_wordlen_2.csv','w')
outsent = open('train70long_sentlen_2.csv','w')

totalwordlen = []
totalsentlen = []
totalwordcounts = {}

#label outcount and outword docs
infile = open('top10000.txt','r') #not stemmed
top10k = infile.readlines()
infile.close()
for w in top10k:
#    outfreq.write(str(w[:-1] + ',')) don't write yet, there are dupes
#    outcount.write(str(w[:-1] + ',')) don't write yet, there are dupes
    totalwordcounts[w[:-1]] = 0 # {'other': 0, 'take': 0, ...}

top10k = []

def doitall(docs): #must be split
    for doc in docs[:1]:
        #headers: the,of,is,...
        infile = open(datadir + doc[:-1],'r') #[:-1] = no \n
        text = infile.read().decode('utf-8', 'ignore').split()
        infile.close()
        outfreq.write(str(uf.top10k(text)[0])[1:-1] + '\n')
        outcount.write(str(uf.top10kcounts(text)[0])[1:-1] + '\n')
    c = 0
    for doc in docs:
        if c == 0:
            pass
        elif c % 100 == 0:
            print c
        else:
            pass
        infile = open(datadir + doc[:-1],'r') #[:-1] = no \n
        text = infile.read().decode('utf-8', 'ignore').split()
        infile.close()

        if len(text) == 0: #empty post
            outfreq.write(('0,' * 9989)[:-1] + '\n')
            #9991 WL, SL, top10000
            outcount.write(('0,' * 9989)[:-1] + '\n')
        else:
            outfreq.write(str(uf.top10k(text)[1])[1:-1] + '\n')
            outcount.write(str(uf.top10kcounts(text)[1])[1:-1] + '\n')

        for word in text:
            word = word.lower()
            if word in totalwordcounts:
                totalwordcounts[word] += 1
            
        totalwordlen.append(uf.avgwordlength(text))
        totalsentlen.append(uf.avgsentlength(text))
        c += 1

datadir = '/Users/robin/Documents/Thesis_local/corpora/blogs/train70/' #data directory
infile = open('train70.txt','r')

##datadir = 'blogtrain/' #data directory
##infile = open('blogtrain.txt','r')
train70docs = infile.readlines()
infile.close()

doitall(train70docs)

##totalavgwordlen = sum(totalwordlen) / float(len(totalwordlen))
##totalavgsentlen = sum(totalsentlen) / float(len(totalsentlen))

for i in totalwordlen:
    s = str(i) + '\n'
    outword.write(s)

for i in totalsentlen:
    s = str(i) + '\n'
    outsent.write(s)

for i in totalwordcounts:
    s = str(i) + ',' + str(totalwordcounts[i]) + '\n'
    totcount.write(s)

outfreq.close()
outsent.close()
outword.close()
outcount.close()
totcount.close()
