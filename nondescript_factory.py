# break doc into 7 parts
# run cosine sim on each pair in those 7
# perform nondescript language transformation on 1 doc
# run cosine sim again
# return the average similarity change 

##    nondescript_factory.py [data directory] [list of filenames] \
## [filename for results] [directory for nondescripted files]


from sys import argv
import cosinesim as sim
import nondescript as nd
import textwrap

##datadir = argv[1] #directory of data
##doclistfile = open(argv[2],'r') #files in that dir
datadir = '/Users/robin/Documents/Thesis_local/corpora/blogs/train70' #directory of data
doclistfile = open('train70.txt','r') #files in that dir
doclist = doclistfile.readlines()
doclistfile.close()

results = open('nondescript_factory_results.txt','w')
#results = argv[3] #filename for results 
#nddump = argv[4] #where to put files that have undergone nondescript transformation

docs = []

for d in doclist:
    docs.append(d[:-1]) #ignore \n

def preptext(docname):
    '''preptext(documentName) -> opens file, scrapes just content'''
    results.write('\n-----------------------------------------------\n')
    results.write(docname)
    print docname
    results.write('\n')
    doclist.append(docname) #add 
    infile = open(datadir + '/' + docname,'r')
    text = infile.read().decode('utf-8', 'ignore')
    infile.close()
    return text

for doc in docs[:10]:
    text = preptext(doc)
    chunks = textwrap.wrap(text, len(text)/7, break_long_words = False) #break doc into 7 chunks
##    normsimall = []
##    for c in chunks:
##        if len(c) < 2000: #sometimes textwrap splits text with one last tiny document
##            chunks = chunks[:-1]
##        else:
##            normsim = []
##            print len(c)
##            for d in chunks:
##                score = sim.main(c[-1],d)[0,1]
##                results.write(str(score)) #cosine similarity for each doc pair in chunks
##                normsim.append(score)
##                normsimall.append(score)
##                results.write('\n')
##            results.write(('---set average: ' + str(sum(normsim) / len(normsim)) + '\n')) #exclude self 1.0?

    normsimall = []

    if len(chunks[-1]) < 5000: #sometimes textwrap splits text with one last tiny document
        chunks = chunks[:-1]
    else:
        pass
    for c in chunks:
        normsim = []
        print len(c)
        print len(chunks[-1])
        score = sim.main(chunks[-1],c)[0,1] #compare the final doc to everything else
        results.write((str(score) + '\t\t' + c[:20])) #cosine similarity for each doc pair in chunks
        #normsim.append(score)
        normsimall.append(score)
        results.write('\n')
        #results.write(('---set average: ' + str(sum(normsim) / len(normsim)) + '\n')) #exclude self 1.0?  
    results.write(('---total average: ' + str(sum(normsimall) / len(normsimall)) + '\n'))
    results.write('\n*********************************\n')
    newdoc = nd.main(chunks[-1]) #transform the final doc
    chunks = chunks[:-1] #remove original final doc
    chunks.append(newdoc) #add transformed final doc
    newsim = []
    for c in chunks:
        score = sim.main(chunks[-1],c)[0,1]
        results.write((str(score) + '\t\t' + c[:20])) #cosine similarity for each doc pair in chunks vs last doc has undergone transformation
        newsim.append(score)
        results.write('\n')
    results.write(('---new average: ' + str(sum(newsim) / len(newsim)) + '\n')) #exclude self 1.0


results.close()
