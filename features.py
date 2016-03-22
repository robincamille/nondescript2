# Finds features in given list of documents
# Performs Gaussian NB on them
# Returns accuracy

# Current features: 10k most common words, according to Google Ngrams

from random import randint
import nltk, nondescript
from numpy import genfromtxt
from sklearn.naive_bayes import GaussianNB
sentsplitter = nltk.data.load('tokenizers/punkt/english.pickle')
stemmer = nltk.stem.PorterStemmer()

outfile = open("features_blogtrain.csv","w")

datadir = 'blogtrain' #data directory
infile = open('blogtrain.txt','r')
documents = infile.readlines()
infile.close()

##top100words = ['the','be','to','of','and','a','in','that','have','I','it','for','not','on','with','he','as','you','do','at','this','but','his','by','from','they','we','say','her','she','or','an','will','my','one','all','would','there','their','what','so','up','out','if','about','who','get','which','go','me','when','make','can','like','time','no','just','him','know','take','people','into','year','your','good','some','could','them','see','other','than','then','now','look','only','come','its','over','think','also','back','after','use','two','how','our','work','first','well','way','even','new','want','because','any','these','give','day','most','us']
## ^ From OED study
##top = [['the',0],['be',0],['to',0],['of',0],['and',0],['a',0],['in',0],['that',0],['have',0],['I',0],['it',0],['for',0],['not',0],['on',0],['with',0],['he',0],['as',0],['you',0],['do',0],['at',0],['this',0],['but',0],['his',0],['by',0],['from',0],['they',0],['we',0],['say',0],['her',0],['she',0],['or',0],['an',0],['will',0],['my',0],['one',0],['all',0],['would',0],['there',0],['their',0],['what',0],['so',0],['up',0],['out',0],['if',0],['about',0],['who',0],['get',0],['which',0],['go',0],['me',0],['when',0],['make',0],['can',0],['like',0],['time',0],['no',0],['just',0],['him',0],['know',0],['take',0],['people',0],['into',0],['year',0],['your',0],['good',0],['some',0],['could',0],['them',0],['see',0],['other',0],['than',0],['then',0],['now',0],['look',0],['only',0],['come',0],['its',0],['over',0],['think',0],['also',0],['back',0],['after',0],['use',0],['two',0],['how',0],['our',0],['work',0],['first',0],['well',0],['way',0],['even',0],['new',0],['want',0],['because',0],['any',0],['these',0],['give',0],['day',0],['most',0],['us',0]]

infile = open('top10000.txt','r') #not stemmed
top10000 = infile.readlines()
infile.close()

def top100(text): #currently top10000
    """Returns array of frequencies for only top 100 words in English (OED)"""
    text = text.split()
    top100dict = {}
    for word in top10000:
    #for word in top100words:
        top100dict[word[:-1]] = 0 # {'other': 0, 'take': 0, ...}
        
    for word in text:
        #word = stemmer.stem(word)
        word = word.lower()
        if word in top100dict:
            top100dict[word] += 1
    top100freqs = []
    for key, value in sorted(top100dict.items()):
        top100freqs.append(value/float(len(text)))
    return top100freqs # [0.03731343283582089, 0.007462686567164179,...]

def addrandom(text):
    #put random phrases in 10% of documents
    randoms = []
    numrandom = len(documents)/50
    while numrandom > 0:
        randoms.append(randint(0,len(documents)))
        numrandom -=1
    
i = 0
for doc in documents:
    #print doc
    infile = open(datadir + '/' + doc[:-1],'r') #[:-1] = no \n
    text = infile.read().decode('utf-8', 'ignore')
    infile.close()

    #put in random phrases
    if i in randoms:
        #pass
        text = nondescript.main(text)

    #create array
    if len(text.split()) == 0: #empty post
        outfile.write(('0,' * 9989)[:-1] + '\n')
        #9991 WL, SL, top10000
    else:
        outfile.write(str(top100(text))[1:-1] + '\n')
        #outfile.write(str(avgsentlength(text)) + ',' + str(avgwordlength(text)) + ',' + str(top100(text))[1:-1] + '\n')
    i += 1

outfile.close()

data = genfromtxt('features_blogtrain.csv', delimiter=',')
targets = genfromtxt('blogtrain_simple.txt', delimiter=',') #targets must be numeric

gnb = GaussianNB()
y_pred = gnb.fit(data, targets).predict(data)
print("Number of mislabeled points out of a total %d points : %d"
      % (data.shape[0],(targets != y_pred).sum()))
print ("Accuracy: %f" % ((targets == y_pred).sum() / float(data.shape[0]) * 100))

##def gaussNB(data,targets,docnames): 
##    '''gaussNB(dataset,targets,documentNames) -> mean accuracy + output prediction file'''
##gnb = GaussianNB()
##preds = gnb.fit(data, targets).predict(data)
##print 'Number of mislabeled points out of a total %d points : %d' \
##      % (data.shape[0],(targets != preds).sum())
##score = 'Score: %f' % gnb.score(data,targets)
##print score
##outputfile(preds,targets,docnames)
##joblib.dump(gnb,useclassifier) #save classifier
##
##
##datadir = 'blogtest' #data directory
##infile = open('blogtest.txt','r')
##testdocnames = infile.readlines()
##infile.close()
##
##
##gnbtest = joblib.load(useclassifier) #must have saved a classifier previously
##preds = gnbtest.fit(datatest,targetstest).predict(datatest)
##print 'Number of mislabeled points out of a total %d points : %d' \
##      % (datatest.shape[0],(targetstest != preds).sum())
##score = 'Score: %f' % gnbtest.score(datatest,targetstest)
##print score
##outputfile(preds,targetstest,testdocnames)


