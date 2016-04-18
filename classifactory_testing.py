# Opens 10 devtest files, split into 2 parts, try out classifier
#Tests classifier script, classifactory.py, with devtest documents.
#Each document is classified 30 times:
#5 times each with the real and anonymized messages, considering
#100-, 1000-, or 10000-word vocabulary size.

#Output example:
#1566807.female.37.Education.Gemini.xml,real,10000,attributed,0.938
#Filename,real/anon,100/1k/10k,(not_)attributed,classifierAccuracy


from classifactory import classifydocs
from  more_itertools import chunked
from nondescript import changewords

##doc = open('compare-doc.txt','r')
##docraw = doc.read()
##doc.close()
##
##msg = open('message-doc.txt','r')
##message = msg.read()
##msg.close()

with open('test_over280kbytes.txt') as dev:
    devs = [l[:-1] for l in dev]
    
listdir = '/Users/robin/Documents/Thesis_local/corpora/blogs/test/'

outfile = open('test_results/test_results_test40_voc-tf-smoothed_1-40_1000.csv','w')

alldata = []

def testdocset(dsample, dmessage, listdata):
    nums = [100,1000,10000]
    threelists = []
    for n in nums[1:2]:
        fivelists = []
        print n
        j = 0
        while j < 5:
            newlist = list(listdata)
            newlist.append(n)
            print 'Random set', j
            printclassify = [i for i in classifydocs('/Users/robin/Documents/Thesis_local/corpora/blogs/train/',\
                                                         'train_above280Kbytes.txt',\
                                                         dsample,\
                                                         dmessage,\
                                                         #anonmessage,\
                                                         n)]
            newlist.append(printclassify)
            j += 1
            fivelists.append(newlist)
        threelists.append(fivelists)
    return threelists
        

doccount = 1
for doc in devs[:40]:
    print '\n===================', doccount, '==================='
    print doc
    testdata = []
    testdataanon = []
    testdata.append(doc)
    testdataanon.append(doc)
    with open(listdir + doc) as d:
        d = d.read()
        d = d.split()
        dsample = d[:15000] #15000 word sample
        dsample = ' '.join(dsample)
        dmessage = d[20000:25000] #5000 word message
        dmessage = ' '.join(dmessage)
        danon = changewords(dmessage)[1] #i'm feeling lucky: random synonyms
    testdata.append('real')
    alldata.append(testdocset(dsample, dmessage, testdata))
    testdata.append(doc)
    testdataanon.append('anon')
    alldata.append(testdocset(dsample, danon, testdataanon))
    doccount += 1


for l in alldata:
    for ll in l:
        outfile.write(str(ll))
        outfile.write('\n')

outfile.close()
print '\nDone'
