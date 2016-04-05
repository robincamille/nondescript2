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
            w2 = w
            s = 0
            wlist = []
            while w2.lower() == w:
                i = randint(0,len(syn)-1)
                w2 = syn[i].lemma_names[0]
                s += 1
                wlist.append(w2)
                if s == len(syn)-1:
                    break
            textprint.append(w2.upper())
        else:
            textprint.append(w)
    return ' '.join(textprint)

