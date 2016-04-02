# avg freq for 10k words across 16689 docs in train70 corpus

import csv

outavg = open('train_all-freqs_smoothed_avg.csv','w')

allwords = []

c = 0
while c < 10000:
    allwords.append(0.0)
    c += 1

print len(allwords)

#collapse all rows into single summed row
inf = open('train_freqs_smoothed.csv','r')
fq = inf.readlines()

for word in fq[0]:
    outavg.write(word)

outavg.write('\n')

for row in fq[2:]:
    i = 0 #i will iterate through all 10k columns
    for v in row.split(','):
        allwords[i] += float(v)
        i +=1
    #print r
    #r += 1

##outtot = open('train70_all-counts_2.csv','w')
####now completed in uniquefeatures_do-all.py
##for a in allwords:
##    a = str(a) + ','
##    outtot.write(a)

for s in allwords:
    s = s / 750.0
    s = str(s) + ','
    outavg.write(s)

##outtot.close()
outavg.close()
inf.close()

