# This script handles the Flask site: shuttles data back and forth
# between the web interface and the Nondescript Python scripts.
# Text output is minimally formatted.

# Must fix: directory & filename in line 98 (specific to my local machine)

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

# Main page (first input)
@app.route('/')
def my_form():
    return render_template("compare-form.html")

# Output page
@app.route('/', methods=['GET','POST'])
def my_form_post():

    # Nondescript UI input page: left box, writing sample
    # same as output page: invisible
    corpus = request.form['corpus'] 

    # Nondescript UI input page: right box, message
    # Output page: 3 tabs at the bottom
    if request.form['whichmessage'] == 'choosesuggestmessage':
        message = request.form['suggestmessage']
    if request.form['whichmessage'] == 'chooseluckymessage':
        message = request.form['luckymessage']
    if request.form['whichmessage'] == 'chooseorigmessage':
        message = request.form['origmessage']
        
    docraw = corpus + ' ' + message #Analyze writing overall 
    doc = docraw.split()
    printcompare = [] #things to print: style vs. all background documents
    printoverall = [] #things to print: overall style
    printclassify = [] #things to print: classifier output


    #Set up word frequency comparison
    with open('train_top1000_all-freqs_smoothed_avg_2col.csv') as infile:
        allfreqraw = [l for l in infile]
    allfreq = {}
    for row in allfreqraw:
        row = row.split(',')
        allfreq[row[0][:-1]] = float(row[1])
    
    #Document length
    #s.append('Document length: %d words' % len(doc))

    #Return message forms: synonym-suggestion, -replacement, original
    origmessage = message
    anonmessage = changewords(message)
    suggestmessage = anonmessage[0] #includes synonym suggestions in parens
    luckymessage = anonmessage[1] #randomly replaces some words with synonyms

    #Cosine similarity in vocabularies of 100, 1000, 10000 words
    printcompare.append('Similarity between this message and original writing sample (10k words): %.3f'\
                        % (sim(toponly.top(corpus,10000),toponly.top(message,10000))[0,1]))
    printcompare.append('Similarity between this message and original writing sample (1k words): %.3f' \
                        % (sim(toponly.top(corpus,1000),toponly.top(message,1000))[0,1]))
    printcompare.append('Similarity between this message and original writing sample (100 words): %.3f'   \
                        % (sim(toponly.top(corpus,100),toponly.top(message,100))[0,1]))

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

    for word in doc:
        doccount[word.lower()] += 1 #term count

    for word in doccount: 
        docfreq[word] = doccount[word] / float(len(doccount)) #term frequency

    #Compare to 7 random authors in background corpus
    #Run through classifier: train & test
    printclassify = [i for i in classifydocs('/Users/robin/Documents/Thesis_local/corpora/blogs/train/',\
                                             'train_above280Kbytes.txt',\
                                             docraw,\
                                             message,\
                                             1000)]


    #Compare word frequencies
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

    #Output to send to compare-output-simple.html
    return render_template("compare-output-simple.html", \
                           compareoverall = printoverall, \
                           corpus = corpus, \
                           repeatdoc = message, \
                           suggestdoc = suggestmessage, \
                           luckydoc = luckymessage, \
                           origdoc = origmessage, \
                           comparestats = printcompare, \
                           classifystats = printclassify)

# About page
@app.route('/about')
def my_form_about():
    return render_template("compare-form-about.html")

if __name__ == '__main__':
    app.debug = True
    app.run()




