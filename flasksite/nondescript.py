# Adds words and phrases to text to anonymize

from random import randint
from nltk.corpus import wordnet as wn
from nltk import word_tokenize as tok

           
def changewords(text):
    i = 0
    text = text.split()
    textprint = []
    for w in text: 
        w = w.lower()
        syn = wn.synsets(w)
        if len(w) < 3:
            textprint.append(w)
        elif 2 < len(syn) < 8:
##            w2 = w
##            s = 0
##            wlist = []
            
##            while w2.lower() == w:
##                i = randint(0,len(syn)-1)
##                w2 = syn[i].lemma_names[0]
##                s += 1
##                wlist.append(w2)
##                if s == len(syn)-1:
##                    break
            s = 0
            wlist = ' ('
            while s < len(syn):
                new = syn[s].lemma_names[0]
                if new.lower() == w:
                    pass
                else:
                    if '_' in new:
                        new = new.split('_')[0] + ' ' + new.split('_')[1]
                    wlist += (new + ', ')
                s += 1
            if len(wlist) < 3:
                textprint.append(w)
            else:
                textprint.append((w.upper() + wlist[:-2] + ')'))
        else:
            textprint.append(w)
    return ' '.join(textprint)

