# This script handles the Flask site: shuttles data back and forth
# between the web interface and the Nondescript Python scripts.
# Text output is minimally formatted.

# Must fix: directory & filename in line 98 (specific to my local machine)

from flask import Flask, request, render_template
from numpy import mean
from collections import defaultdict
from sys import argv
from more_itertools import chunked, unique_everseen as dedup

import toponly
from uniquefeatures import avgwordlength, avgsentlength
from cosinesim import sim
from nondescript import changewords
from random import randint
from buildclassifier import classifydocs
from nltk import word_tokenize as tok
from sources import *

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
    #doc = docraw.split()
    doc = tok(docraw)
    printcompare = [] #things to print: style vs. all background documents
    printoverall = [] #things to print: overall style
    printunusualwords = []
    unusualwordsonly = []
    printclassify = [] #things to print: classifier output
    advice = [] #tips such as use shorter sentences

    
    #Document length
    #s.append('Document length: %d words' % len(doc))

    #Return message forms: synonym-suggestion, -replacement, original
    origmessage = message
    anonmessage = changewords(message)
    suggestmessage = anonmessage[0] #includes synonym suggestions in parens
    luckymessage = anonmessage[1] #randomly replaces some words with synonyms

    #Cosine similarity in vocabularies of 100, 1000, 10000 words
    printcompare.append('Similarity between this message and original writing sample: %.3f'\
                        % (sim(toponly.top(corpus,10000),toponly.top(message,10000))[0,1]))
    # printcompare.append('Similarity between this message and original writing sample (10k words): %.3f'\
    #                     % (sim(toponly.top(corpus,10000),toponly.top(message,10000))[0,1]))
    # printcompare.append('Similarity between this message and original writing sample (1k words): %.3f' \
    #                     % (sim(toponly.top(corpus,1000),toponly.top(message,1000))[0,1]))
    # printcompare.append('Similarity between this message and original writing sample (100 words): %.3f'   \
    #                     % (sim(toponly.top(corpus,100),toponly.top(message,100))[0,1]))

    #Average word lengths
    printcompare.append("Your message's word length is {:.2f}x \
        your average".format(avgwordlength(message.split())/avgwordlength(corpus.split())))
    #totwlavg = mean(totwl)
    word_compare = avgwordlength(doc)/backgroundcorpusWL
    if word_compare > 1.2:
        advice.append("Try using shorter words.")
    elif word_compare < 0.9:
        advice.append("Try using longer words.")
    printoverall.append("Your overall word length is {:.2f}x \
        everyone else's average.".format(word_compare))

    #Average sent lengths
    printcompare.append("Your message's sentence length is {:.2f}x \
        your average".format(avgsentlength(message)/avgsentlength(corpus)))
    #totslavg = mean(totsl)
    sent_compare = avgsentlength(doc)/backgroundcorpusSL
    if sent_compare > 1.2:
        advice.append("Try shorter sentences.")
    elif sent_compare < 0.9:
        advice.append("Try longer sentences.")
    printoverall.append("Your overall sentence length is {:.2f}x \
        everyone else's average.".format(sent_compare))
    
    advice.append("Focus on changing the red-underlined words.")



    #Top unusual words
    
    #Set up word frequency comparison
    with open(bcfreqs) as infile: #from sources.py
        allfreqraw = [l[1:] for l in infile]
    allfreq = {}
    for row in allfreqraw:
        row = row.split(',')
        allfreq[row[0][:-1]] = float(row[1])

    # with open('allfreq.csv','w') as allfreqfile:
    # 	allfreqfile.write(str(allfreq))

    doccount = defaultdict(int)
    docfreq = defaultdict(int)

    for word in doc:
        doccount[word.lower()] += 1 #term count

    for word in doccount: 
        docfreq[word] = doccount[word] / float(len(doccount)) #term frequency

    # with open('docfreq.csv','w') as docfreqfile:
    # 	docfreqfile.write(str(docfreq))

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
                # if compfreq[word][1] == 0:
                #     v = compfreq[word][1] / minfreq #min freq from train/
                # else:
                v = compfreq[word][0] / float(compfreq[word][1])
                compwords.append([v, word, doccount[word]]) #currently 0 words? fix this
            else:
                pass
        else:
            pass

    printoverall.append('Five most unusual words overall, compared with an average document:')
    compwordssort = sorted(compwords,reverse=True)
    
    for i in compwordssort[:5]:
    	unusualwordsonly.append(i[1])
        printunusualwords.append('%15s %4.2fx more frequent (used %d times)' % (i[1],i[0],i[2]))



    # The important bit: 

    #Compare to n random authors in background corpus
    #Run through classifier: train & test
    #backgroundcorpus directory & filelist .txt file specified
    #in sources.py
    classifieroutcome = [i for i in classifydocs(backgroundcorpus,\
                                             filelist,\
                                             docraw,\
                                             message,\
                                             1000)] #vocab of n words




    #Output to send to compare-output-simple.html
    return render_template("compare-output-simple.html", \
                           compareoverall = printoverall, \
                           # unusualwordsonly = unusualwordsonly, \
                           unusualwords = printunusualwords, \
                           advice = advice, \
                           corpus = corpus, \
                           repeatdoc = message, \
                           suggestdoc = suggestmessage, \
                           luckydoc = luckymessage, \
                           origdoc = origmessage, \
                           comparestats = printcompare, \
                           classifieroutcome = classifieroutcome[0], \
                           classifierscore = classifieroutcome[1])

# About page
@app.route('/about')
def my_form_about():
    return render_template("compare-form-about.html")

if __name__ == '__main__':
    app.debug = True
    app.run()




