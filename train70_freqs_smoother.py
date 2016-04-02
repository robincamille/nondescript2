# add laplace smoothing to train70 word freq sparse matrix
# smallest value in all averaged word freqs in train 70:
# 0.0000000068378075535599996864288668536966536715127062961983028799295425415039062500000000000000000000


inf = open('train_freqs.csv','r')
f = inf.readlines()
inf.close()

out = open('train_freqs_smoothed.csv','w')

c = 0

for i in f[0]: #header line
    out.write(i)
#out.write('\n') #included

train70 = '0.0000000068378'
train70long = '0.000018'
train70longf = 0.000018
trainalls = '0.0000000176'
trainallf = 0.0000000176

for line in f[1:]:
    for i in line.split(','):
        if str(i) == '0':
            g = trainalls + ','
        elif str(i) == ' 0.0': 
            g = trainalls + ','
        elif str(i) == '0.0': 
            g = trainalls + ','
        elif str(i) == '0.0\n': #end of line
            g = trainalls
        elif str(i) == ' 0.0\n': #end of line
            g = trainalls
        elif str(i)[-1] == '\n':
            g = str(float(i[:-1]) + trainallf)
        elif str(i)[0] == ' ':
            g = str(float(i[1:]) + trainallf) + ','
        else:
            g = str(float(i) + trainallf) + ','
        out.write(g)
    out.write('\n')

out.close()
