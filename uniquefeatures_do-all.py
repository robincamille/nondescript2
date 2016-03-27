import uniquefeatures as uf

#outfreq = open('train70_freqs.txt','w')
outword = open('train70_wordlen.txt','w')
outsent = open('train70_sentlen.txt','w')

totalwordlen = []
totalsentlen = []

def doitall(docs): #must be split

    for doc in docs:
        infile = open(datadir + doc[:-1],'r') #[:-1] = no \n
        text = infile.read().decode('utf-8', 'ignore').split()
        infile.close()

##        if len(text) == 0: #empty post
##            outfreq.write(('0,' * 9989)[:-1] + '\n')
##            #9991 WL, SL, top10000
##        else:
##            outfreq.write(str(top10k(text))[1:-1] + '\n')
            
        #getfreq(text)
        totalwordlen.append(uf.avgwordlength(text))
        totalsentlen.append(uf.avgsentlength(text))

datadir = '/Users/robin/Documents/Thesis_local/corpora/blogs/train70_split/' #data directory
infile = open('train70.txt','r')
train70docs = infile.readlines()
infile.close()

doitall(train70docs)

totalavgwordlen = sum(totalwordlen) / float(len(totalwordlen))
totalavgsentlen = sum(totalsentlen) / float(len(totalsentlen))

for i in totalwordlen:
    s = str(i) + '\n'
    outword.write(s)

for i in totalsentlen:
    s = str(i) + '\n'
    outsent.write(s)


#outfreq.close()
outsent.close()
outword.close()
