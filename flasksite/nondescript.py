# Adds words and phrases to text to anonymize

from random import randint
from nltk.corpus import wordnet as wn
from nltk import word_tokenize as tok

ignore = ['will','must','there']
           
def changewords(text):
    i = 0
    text = text.split()
    textprint = []
    for w in text: 
        w = w.lower()
        syn = wn.synsets(w)
        if len(w) < 3:
            textprint.append(w)
        elif w.lower() in ignore:
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
            wlist = []
            for s in range(len(syn)-1):
                newall = syn[s].lemma_names() # () for air
                for new in newall:
                    if new.lower() == w:
                        pass
                    if new in wlist:
                        pass
                    else:
                        if '_' in new:
                            new = new.split('_')
                            new = ' '.join(new)
                        wlist.append(new)
            wprint = ' ('
            for n in wlist[1:]:
                wprint += (n + ', ')
            if len(wlist) < 3:
                textprint.append(w)
            else:
                textprint.append((w.upper() + wprint[:-2] + ')'))
        else:
            textprint.append(w)
    return ' '.join(textprint)

