from flask import Flask, request, render_template
from uniquefeatures import avgwordlength, avgsentlength
from numpy import mean
from collections import defaultdict
from sys import argv
from cosinesim import sim
from nondescript import changewords
import toponly
from  more_itertools import unique_everseen as dedup

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template("compare-form.html")

@app.route('/', methods=[',GET','POST'])
def my_form_post():

    corpus = request.form['corpus'] #'corpus' is the textarea name (left)
    message = request.form['message'] #'message' is the textarea name (right)

    docraw = corpus + ' ' + message
    doc = docraw.split()
    printcompare = []
    printoverall = [] #things to print: overall style

##    #Set up word length calculator
##    with open('train_wordlen.csv') as infile:
##        totwl = [float(l[:-1]) for l in infile]
##
##    #Set up sentence length calculator
##    with open('train_sentlen.csv') as infile:
##        totsl = [float(l[:-1]) for l in infile]


    #Set up word frequency compare-er
    #File from 70 authors'
        
##    freqfiles = [open('train_all-freqs_smoothed_avg_2col.csv','r'),open('train_top1000_all-freqs_smoothed_avg_2col.csv','r'),open('train_top100_all-freqs_smoothed_avg_2col.csv','r')]
##    for freqfile in freqfiles:
##        freqfileraw = freqfiles.readlines()
##        freqfile.close()
##        
##        allfreq = {}
##        for row in allfreqraw:
##            row = row.split(',')
##            allfreq[row[0][1:-1]] = float(row[1]) #row[0] is 'aaron' hence [1:-1]


    with open('train_top100_all-freqs_smoothed_avg_2col.csv') as infile:
        allfreqraw = [l for l in infile]
    allfreq = {}
    for row in allfreqraw:
        row = row.split(',')
        allfreq[row[0][1:-1]] = float(row[1]) #row[0] is 'aaron' hence [1:-1]
    

    #Document length
    #s.append('Document length: %d words' % len(doc))

    #Return anonymized message
    anonmessage = changewords(message)

    #Cosine similarity
    
    printcompare.append('Similarity between this message and original writing sample (10k words): %.3f'\
                        % (sim(toponly.top(corpus,10000),toponly.top(message,10000))[0,1]))
    printcompare.append('Similarity between this message and original writing sample (1k words): %.3f' \
                        % (sim(toponly.top(corpus,1000),toponly.top(message,1000))[0,1]))
    printcompare.append('Similarity between this message and original writing sample (100 words): %.3f'   \
                        % (sim(toponly.top(corpus,100),toponly.top(message,100))[0,1]))
    #anonsim = ('Similarity between suggested message and original writing sample: %.3f' \
    #   % (sim(toponly.top(corpus),toponly.top(anonmessage))[0,1]))


    #Average word lengths
    printcompare.append("Your message's word length is %.2fx your average" \
                        % (avgwordlength(message.split())/avgwordlength(corpus.split())))
    #totwlavg = mean(totwl)
    printoverall.append("Your overall word length is %.2fx everyone else's average"  \
                        % (avgwordlength(doc)/6.8916756214142039))

    #Average sent lengths
    printcompare.append("Your message's sentence length is %.2fx your average" \
                        % (avgsentlength(message)/avgsentlength(corpus)))
    #totslavg = mean(totsl)
    printoverall.append("Your overall sentence length is %.2fx everyone else's average" \
                        % (avgsentlength(doc)/104.33064342040956))             
    #Top unusual words
    doccount = defaultdict(int)
    docfreq = defaultdict(int)

    #print 'Term counting'
    for word in doc:
        doccount[word.lower()] += 1 #term count

    #print 'Term frequencies'
    for word in doccount: 
        docfreq[word] = doccount[word] / float(len(doccount)) #term frequency

    #print 'Comparing to all docs'
    compfreq = defaultdict(list)
    for word in docfreq:
        if word in allfreq.keys():
            compfreq[word] = [docfreq[word],allfreq[word]]
        else:
            pass

    compwords = []
    for word in compfreq:
        if doccount[word] > 1:
            if compfreq[word][0] > compfreq[word][1]:
                if compfreq[word][1] == 0:
                    v = compfreq[word][1] / 0.0000000176 #min freq from train/
                else:
                    v = compfreq[word][0] / float(compfreq[word][1])
                compwords.append([v, word, doccount[word]])
            else:
                pass
        else:
            pass

    printoverall.append('Most unusual words overall, compared with an average document:')
    compwordssort = sorted(compwords,reverse=True)
    
    for i in compwordssort[:10]:
        printoverall.append('%15s %4.2fx more frequent (used %d times)' % (i[1],i[0],i[2]))


    return render_template("compare-output-simple.html", \
                           compareoverall = printoverall, \
                           corpus = corpus, \
                           repeatdoc = message, \
                           anondoc = anonmessage, \
                           comparestats = printcompare)
    
if __name__ == '__main__':
    app.debug = True
    app.run()




