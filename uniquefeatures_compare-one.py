# individual document compared to train70 corpus

from uniquefeatures import avgwordlength, avgsentlength
from numpy import mean
from collections import defaultdict

#Set up word length calculator
infile = open('train70long_wordlen_2.csv','r')
totwlraw = infile.readlines()
infile.close()

totwl = []
for i in totwlraw:
    totwl.append(float(i[:-1]))
    
#Set up sentence length calculator
infile = open('train70long_sentlen_2.csv','r')
totslraw = infile.readlines()
infile.close

totsl = []
for i in totslraw:
    totsl.append(float(i[:-1]))

#Set up word frequency compare-er
    #File from 70 authors' documents
infile = open('train70long_all-freqs_2_smoothed_avg_2col.csv','r')
allfreqraw = infile.readlines()
infile.close()

allfreq = {}
for row in allfreqraw:
    row = row.split(',')
    allfreq[row[0][1:-1]] = float(row[1]) #row[0] is 'aaron' hence [1:-1]
    
infile = open('testdoc2.txt','r')
doc = infile.read().decode('utf-8','ignore').split()
infile.close()
#not properly tokenized!!!!! ------------------------------

#Document length
print 'Document length: %d words' % len(doc)

#Average word lengths
totwlavg = mean(totwl)
print 'Word length is %.2fx average' % (avgwordlength(doc)/float(totwlavg))

#Average sent lengths
totslavg = mean(totsl)
print 'Sentence length is %.2fx average' % (avgsentlength(doc)/float(totslavg))

#Top unusual words
doccount = defaultdict(int)
docfreq = defaultdict(int)

#print 'Term counting'
for word in doc:
    word = word.lower()
    doccount[word] += 1 #term count

#print 'Term frequencies'
for word in doccount:
    docfreq[word] = doccount[word] / float(len(doc)) #term frequency

#print 'Comparing to all docs'
compfreq = defaultdict(list)
for word in docfreq:
    if word in allfreq.keys():
        compfreq[word] = [docfreq[word],allfreq[word]]
    else:
        pass

compwords = []
for word in compfreq:
    if compfreq[word][0] > compfreq[word][1]:
        if compfreq[word][1] == 0:
            v = compfreq[word][1] / 0.0000000068378075535599996
        else:
            v = compfreq[word][0] / float(compfreq[word][1])
        compwords.append([v, word, doccount[word]])
    else:
        pass

print '\nTop words:'
compwordssort = sorted(compwords,reverse=True)
for i in compwordssort[:25]:
    print '%15s %.2fx more frequent than average document\t(%d times)' % (i[1],i[0],i[2])


# smallest value in all averaged word freqs in train 70 split:
# 0.0000000068378075535599996864288668536966536715127062961983028799295425415039062500000000000000000000
