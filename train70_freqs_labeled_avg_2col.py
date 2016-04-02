# avg freq for 10k words across 16689 docs in train70 corpus

import csv

outavg = open('try_train_all-freqs_smoothed_avg_2col.csv','w')
numdocs = 2977

allfreqs = []

c = 0
while c < 9989:
    allfreqs.append(0.0)
    c += 1

print len(allfreqs)

#collapse all rows into single summed row
inf = open('train_data/train_freqs_smoothed.csv','r')
fq = inf.readlines()

words = []
for word in fq[0].split(','): #'a','aaa','aaron',...
    words.append(word) #includes line-leading space

#outavg.write('\n') #included

for row in fq[2:]:
    i = 0 #i will iterate through all 10k columns
    for v in row.split(','):
        allfreqs[i] += float(v)
        i +=1
    #print r
    #r += 1

##outtot = open('train70_all-counts_2.csv','w')
####now completed in uniquefeatures_do-all.py
##for a in allwords:
##    a = str(a) + ','
##    outtot.write(a)

i = 0
for s in allfreqs:
    s = s / float(numdocs)
    s = words[i] + ',' + str(s) + '\n' #'a',0.02404...
    outavg.write(s)
    i += 1 #gets tripped up here, last word ends in \n

##outtot.close()
outavg.close()
inf.close()

