# add laplace smoothing to train70 word freq sparse matrix
# smallest value in all averaged word freqs in train 70:
# 0.0000000068378075535599996864288668536966536715127062961983028799295425415039062500000000000000000000


inf = open('train70_freqs_2.csv','r')
f = inf.readlines()
inf.close()

out = open('train70_freqs_2_smoothed.csv','w')

c = 0

for i in f[0]: #header line
    out.write(i)
out.write('\n')

for line in f[1:]:
    for i in line.split(','):
        if str(i) == '0':
            g = '0.0000000068378,'
        elif str(i) == ' 0.0': 
            g = '0.0000000068378,'
        elif str(i) == '0.0': 
            g = '0.0000000068378,'
        elif str(i) == '0.0\n': #end of line
            g = '0.0000000068378'
        elif str(i) == ' 0.0\n': #end of line
            g = '0.0000000068378'
        elif str(i)[-1] == '\n':
            g = str(float(i[:-1]) + 0.0000000068378)
        elif str(i)[0] == ' ':
            g = str(float(i[1:]) + 0.0000000068378) + ','
        else:
            g = str(float(i) + 0.0000000068378) + ','
        out.write(g)
    out.write('\n')

out.close()
