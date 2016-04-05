from flask import Flask
from flask import request
from flask import render_template
from uniquefeatures import avgwordlength, avgsentlength
from numpy import mean
from collections import defaultdict
from sys import argv
from cosinesim import sim
from nondescript import changewords
import toponly

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

    #Set up word length calculator
    infile = open('train_wordlen.csv','r')
    totwlraw = infile.readlines()
    infile.close()

    totwl = []
    for i in totwlraw:
        totwl.append(float(i[:-1]))
        
    #Set up sentence length calculator
    infile = open('train_sentlen.csv','r')
    totslraw = infile.readlines()
    infile.close()

    totsl = []
    for i in totslraw:
        totsl.append(float(i[:-1]))

    #Set up word frequency compare-er
        #File from 70 authors' documents
    infile = open('train_all-freqs_smoothed_avg_2col.csv','r')
    allfreqraw = infile.readlines()
    infile.close()

    allfreq = {}
    for row in allfreqraw:
        row = row.split(',')
        allfreq[row[0][1:-1]] = float(row[1]) #row[0] is 'aaron' hence [1:-1]
    

    #Document length
    #s.append('Document length: %d words' % len(doc))

    #Return anonymized message
    anonmessage = changewords(message)

    #Cosine similarity
    
    printcompare.append('Similarity between this message and original writing sample: %.3f' % (sim(toponly.top(corpus),toponly.top(message))[0,1]))
    #anonsim = ('Similarity between suggested message and original writing sample: %.3f' % (sim(toponly.top(corpus),toponly.top(anonmessage))[0,1]))


    #Average word lengths
    printcompare.append("Your message's word length is %.2fx your average" % (avgwordlength(message)/float(avgwordlength(corpus))))
    totwlavg = mean(totwl)
    printoverall.append("Your overall word length is %.2fx everyone else's average" % (avgwordlength(doc)/float(totwlavg)))

    #Average sent lengths
    printcompare.append("Your message's sentence length is %.2fx your average" % (avgsentlength(message) / float(avgsentlength(corpus))))
    totslavg = mean(totsl)
    printoverall.append("Your overall sentence length is %.2fx everyone else's average" % (avgsentlength(doc)/float(totslavg)))             
    #Top unusual words
    doccount = defaultdict(int)
    docfreq = defaultdict(int)

    #print 'Term counting'
    for word in doc:
        word = word.lower()
        doccount[word] += 1 #term count

    #print 'Term frequencies'
    for word in doccount:
        docfreq[word] = doccount[word] / float(len(doc)) #term frequency

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

    printoverall.append('Most unusual words overall:')
    compwordssort = sorted(compwords,reverse=True)
    
    for i in compwordssort[:10]:
        printoverall.append('%15s %4.2fx more frequent than average document\t(%d times)' % (i[1],i[0],i[2]))


    return render_template("compare-output-simple.html", compareoverall = printoverall, corpus = corpus, repeatdoc = message, anondoc = anonmessage, comparestats = printcompare)
    
if __name__ == '__main__':
    app.debug = True
    app.run()




