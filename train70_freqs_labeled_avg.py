# avg freq 

import csv

allwords = []

c = 0
while c < 10000:
    allwords.append(0)
    c += 1

print len(allwords)

#collapse all rows into single summed row
with open('train70_freqs.csv','r') as csvfile:
    fq = csv.reader(csvfile, delimiter=',')
    r = 0
    for row in fq:
        i = 0 #i will iterate through all 10k columns
        for v in row:
            allwords[i] += float(v)
            i +=1
        print r
        r += 1

print allwords[:5]







csvfile.close()

