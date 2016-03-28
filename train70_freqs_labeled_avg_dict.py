# make dict

inf = open('top10000.txt','r')
topraw = inf.readlines()
inf.close()

top = []
for i in topraw:
    top.append(i[:-1])

inf = open('train70_all-counts_total.csv','r')
freq = inf.read().split(',')
inf.close()

z = zip(top,freq)
d = dict(z)

out = open('train70_all-counts_labeled.csv','w')

for i in d:
    s = i + ',' + d[i] + '\n'
    out.write(s)

out.close()
