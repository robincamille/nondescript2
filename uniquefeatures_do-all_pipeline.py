# for all documents in a given industry, as specified by BAC*, this script
# creates data documents: word frequencies (smoothed, and averaged), word
# counts, average sentence/word lengths.

# this script is a frankenstein's monster of previously written scripts.
# it is not pretty. 

# *BAC = Blog Authorship Corpus; industries are self-selected by blog authors.

import uniquefeatures as uf
import csv

industriesfile = open('train_industries.txt','r')
industries = industriesfile.readlines()
industriesfile.close()

for ind in industries[-2:]:
    ind = ind[:-5] #exclude .txt\n

    print ind
    
    #setup
    outfreq = open('train_by-industry_data/' + ind + '_freqs.csv','w')
    outcount = open('train_by-industry_data/' + ind + '_counts_.csv','w')
    totcount = open('train_by-industry_data/' + ind + '_all-counts.csv','w')
    outword = open('train_by-industry_data/' + ind + '_wordlen.csv','w')
    outsent = open('train_by-industry_data/' + ind + '_sentlen.csv','w')

    datadir = '/Users/robin/Documents/Thesis_local/corpora/blogs/train/' #data directory
    infile = open('train_by-industry/' + ind + '.txt','r')

    inddocs = infile.readlines()
    infile.close()

    totalwordlen = []
    totalsentlen = []
    totalwordcounts = {}

    #label outcount and outword docs
    infile = open('top10000.txt','r') #not stemmed
    top10k = infile.readlines()
    infile.close()
    for w in top10k:
        totalwordcounts[w[:-1]] = 0 # {'other': 0, 'take': 0, ...}

    top10k = []

    def doitall(docs): #must be split
        for doc in docs[:1]: #headers: the,of,is,...
            infile = open(datadir + doc[:-1],'r') #[:-1] = no \n from label file
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
                outfreq.write(('0,' * 9989)[:-1] + '\n') #9989 WL, SL, top10000
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
    print 'Obtaining word counts and frequencies, as well as average word and sentence lengths'
    doitall(inddocs)

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


    # add laplace smoothing to doc word freq sparse matrix
    print 'Smoothing frequencies using Laplace method'
    inf = open('train_by-industry_data/' + ind + '_freqs.csv','r')
    f = inf.readlines()
    inf.close()

    out = open('train_by-industry_data/' + ind + '_freqs_smoothed.csv','w')

    nums = []
    for line in f[1:]:
        allnums = []
        for i in line.split(','):
            if float(i) != 0.0:
                allnums.append(float(i))
        nums.append(min(allnums))
    
    minimums = str(min(nums))
    minimumf = min(nums)
    c = 0

    for i in f[0]: #header line
        out.write(i) #'\n') #included

    for line in f[1:]:
        for i in line.split(','):
            if str(i) == '0':
                g = minimums + ','
            elif str(i) == ' 0.0': 
                g = minimums + ','
            elif str(i) == '0.0': 
                g = minimums + ','
            elif str(i) == '0.0\n': #end of line
                g = minimums
            elif str(i) == ' 0.0\n': #end of line
                g = minimums
            elif str(i)[-1] == '\n':
                g = str(float(i[:-1]) + minimumf)
            elif str(i)[0] == ' ':
                g = str(float(i[1:]) + minimumf) + ','
            else:
                g = str(float(i) + minimumf) + ','
            out.write(g)
        out.write('\n')

    out.close()


    # avg freq for 10k words across all docs in given corpus
    print 'Averaging word frequencies across all documents in', ind
    outavg = open('train_by-industry_data/' + ind + '_all-freqs_smoothed_avg_2col.csv','w')

    allfreqs = []
    c = 0
    while c < 9989:
        allfreqs.append(0.0)
        c += 1
        
    #collapse all rows into single summed row
    inf = open('train_by-industry_data/' + ind + '_freqs_smoothed.csv','r')
    fq = inf.readlines()
    numdocs = len(fq) - 1 #exclude header of 'a','aaa','aaron',...

    words = []
    for word in fq[0].split(','): #'a','aaa','aaron',...
        words.append(word[1:]) #excludes line-leading space

    for row in fq[2:]:
        i = 0 #i will iterate through all 10k columns
        for v in row.split(','):
            allfreqs[i] += float(v)
            i +=1

    i = 0
    for s in allfreqs:
        if i == 9988: #last word in list has \n
            s = s / float(numdocs)
            s = words[i][:-1] + ',' + str(s) + '\n' #'a',0.02404...
        else:
            s = s / float(numdocs)
            s = words[i] + ',' + str(s) + '\n' #'a',0.02404...
        outavg.write(s)
        i += 1 

    outavg.close()
    inf.close()
    print 'Done with', ind, '\n'
