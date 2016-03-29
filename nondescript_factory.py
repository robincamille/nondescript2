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

datadir = argv[1] #directory of data
doclistfile = open(argv[2],'r') #files in that dir
doclist = doclistfile.readlines()
doclistfile.close()

results = argv[3] #filename for results 
nddump = argv[4] #where to put files that have undergone nondescript transformation

for d in doclist:
    docs.append(d[:-1]) #ignore \n

def preptext(docname):
    '''preptext(documentName) -> opens file, scrapes just content'''
    features = []
    doclist.append(docname) #add 
    infile = open(datadir + '/' + docname,'r')
    text = infile.read()
    infile.close()
    for word in text:
        allwords.append(word)
    return text

for doc in docs:
    text = preptext(doc)
    docchunks = textwrap.wrap(text, len(text)/7, break_long_words = False)
    
