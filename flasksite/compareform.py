from flask import Flask, request, render_template
from uniquefeatures import avgwordlength, avgsentlength
from numpy import mean
from collections import defaultdict
from sys import argv
from cosinesim import sim
from nondescript import changewords
import toponly
from more_itertools import chunked, unique_everseen as dedup
from random import randint
from classifactory import classifydocs

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template("compare-form.html")

@app.route('/', methods=['GET','POST'])
def my_form_post():

    corpus = request.form['corpus'] #'corpus' is the textarea name (left)
    
    if request.form['whichmessage'] == 'choosesuggestmessage':
        message = request.form['suggestmessage']
    if request.form['whichmessage'] == 'chooseluckymessage':
        message = request.form['luckymessage']
    if request.form['whichmessage'] == 'chooseorigmessage':
        message = request.form['origmessage']
        
    
    #message = request.form['message'] #'message' is the textarea name (right)

    docraw = corpus + ' ' + message
    doc = docraw.split()
    printcompare = [] #things to print: style vs. all train documents
    printoverall = [] #things to print: overall style
    printclassify = [] #things to print: classifier output


    #Set up word frequency compare-er
    with open('train_top100_all-freqs_smoothed_avg_2col.csv') as infile:
        allfreqraw = [l for l in infile]
    allfreq = {}
    for row in allfreqraw:
        row = row.split(',')
        allfreq[row[0][1:-1]] = float(row[1]) #row[0] is 'aaron' hence [1:-1]
    

    #Document length
    #s.append('Document length: %d words' % len(doc))

    #Return anonymized message
    origmessage = message
    anonmessage = changewords(message)
    suggestmessage = anonmessage[0] #includes synonym suggestions in parens
    luckymessage = anonmessage[1] #randomly replaces some words with synonyms

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
    ##    From:
    ##    with open('train_wordlen.csv') as infile:
    ##        totwl = [float(l[:-1]) for l in infile]

    #Average sent lengths
    printcompare.append("Your message's sentence length is %.2fx your average" \
                        % (avgsentlength(message)/avgsentlength(corpus)))
    #totslavg = mean(totsl)
    printoverall.append("Your overall sentence length is %.2fx everyone else's average" \
                        % (avgsentlength(doc)/104.33064342040956))
    ##    From:
    ##    with open('train_sentlen.csv') as infile:
    ##        totsl = [float(l[:-1]) for l in infile]
    
    #Top unusual words
    doccount = defaultdict(int)
    docfreq = defaultdict(int)

    #print 'Term counting'
    for word in doc:
        doccount[word.lower()] += 1 #term count

    #print 'Term frequencies'
    for word in doccount: 
        docfreq[word] = doccount[word] / float(len(doccount)) #term frequency


    #compare to X random authors
    printclassify = [i for i in classifydocs('/Users/robin/Documents/Thesis_local/corpora/blogs/train/',\
                                             'train_above280Kbytes.txt',\
                                             docraw,\
                                             message,\
                                             #anonmessage,\
                                             10000)]


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

    printoverall.append('Five most unusual words overall, compared with an average document:')
    compwordssort = sorted(compwords,reverse=True)
    
    for i in compwordssort[:5]:
        printoverall.append('%15s %4.2fx more frequent (used %d times)' % (i[1],i[0],i[2]))


    return render_template("compare-output-simple.html", \
                           compareoverall = printoverall, \
                           corpus = corpus, \
                           repeatdoc = message, \
                           suggestdoc = suggestmessage, \
                           luckydoc = luckymessage, \
                           origdoc = origmessage, \
                           comparestats = printcompare, \
                           classifystats = printclassify)


@app.route('/about')
def my_form_about():
    return render_template("compare-form-about.html")

if __name__ == '__main__':
    app.debug = True
    app.run()




