# Outputs two texts:
# changewords(text)[0] has suggestions for replacing words (human-directed).
# changewords(text)[1] has randomly replaced words (automatic).

# New addition: sentences are split with __ as delimiter for textprint (editable area)

from random import randint
from nltk.corpus import wordnet as wn
from nltk import word_tokenize as tok
from wordfilter import Wordfilter

wf = Wordfilter() #https://github.com/dariusk/wordfilter
#Words that may be offensive or that have undesirable results in WordNet:
ignore = ['will','more','must','there','john','screw','queer','crap','shit','ass','sex','fuck','fucker','motherfucker','fucks','fucked','fucking']
           

with open('data/top1000.txt') as vocdoc:
     topwords = [w[:-1] for w in vocdoc.readlines()]

def changewords(text):
    """Returns two texts [T1, T2]: T1 text with certain words (in all caps) followed by
potential synonyms in parentheses, T2 text with randomly-chosen synonyms in all caps
that replace certain words."""
    i = 0
    text = text.split()
    #text = tok(text) - more accurate, but difficult to join below
    textprint = [] #Text will appear as so: she SHOUTED (shout out, call...
    luckyprint = [] #Random synonym will be chosen, as so: She shout out... (No tense consideration)
    for w in text: 
        w = w.lower()
        syn = wn.synsets(w)
        if wf.blacklisted(w) == True: #do nothing with bad words
            textprint.append(w)
            luckyprint.append(w)
        elif len(w) < 3: #do nothing with words with only a few synsets
            textprint.append(w)
            luckyprint.append(w)
        elif w.lower() in ignore: #do nothing with bad words
            textprint.append(w)
            luckyprint.append(w)
        elif 2 < len(syn) < 8: #only consider words with 3-7 synsets
            wlist = []
            for s in range(len(syn)-1):
                try:
                    newall = syn[s].lemma_names() #mysterious errors
                except:
                    newall = syn[s].lemma_names 
                for new in newall:
                    if new.lower() == w: #avoid same word
                        pass
                    elif new in wlist: #avoid duplicates
                        pass
                    elif new[0] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ": #avoid names
                        pass
                    elif wf.blacklisted(new) == True: #avoid bad words
                        pass
                    elif new in ignore: #avoid inappropriate words
                        pass
                    else:
                        if '_' in new: 
                            new = new.split('_') #multi-word expressions
                            new = ' '.join(new)
                        wlist.append(new)
            wprint = '' #link together the parenthetical list of suggestions
            #format (for JS): [[tasks,project,labor,job,chore]]
            for n in wlist[1:]:
                wprint += (n + ',')
                r = randint(0,len(wlist)-1)
                randword = wlist[r] #choose random word for luckyprint
            if len(wlist) < 3:
                textprint.append(w)
                luckyprint.append(w)
            else:
                if w.lower() in topwords:
                    #emphasize urgency of changing considered words
                    textprint.append(('@@' + w + ',' + wprint[:-1] + '@@'))
                else:
                    textprint.append(('[[' + w + ',' + wprint[:-1] + ']]'))
                luckyprint.append(randword.upper())
        else:
            textprint.append(w)
            luckyprint.append(w)
    return ['__'.join(textprint), ' '.join(luckyprint)]

