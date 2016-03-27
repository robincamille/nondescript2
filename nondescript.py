# Adds words and phrases to text to anonymize

from random import randint
from nltk.corpus import wordnet as wn
from nltk import word_tokenize as tok
##from nltk.stem.porter import PorterStemmer
##ps = PorterStemmer()



##filename = open('blogtrain/890034.female.23.indUnk.Scorpio43.txt','r')
##doc = filename.read()
##filename.close()
#text = tok(doc)

phrases = ['I think', 'It seems to me', 'You know', 'If you know what I mean', \
           'Like', 'However', 'So be it', 'It is what it is', 'Really', \
           'To wit', 'Obviously', 'To tell you the truth', 'Trust me', \
           'Damn it', 'Seriously', 'Literally', 'What an opportunity', \
           'You see']
           
def main(text):
    i = 0
    text = text.split()
    while i < 3:
        addphrase = phrases[randint(0,len(phrases)-1)] + ' '
        text.append(addphrase)
        i += 1
    textprint = []
    for w in text: #https://pythonism.wordpress.com/2013/10/07/simple-synonym-replacement/
        #print w
        w = w.lower()
        syn = wn.synsets(w)
        if len(w) < 3:
            textprint.append(w)
        elif 2 < len(syn) < 5:
            s = randint(0,len(syn)-1)
            w2 = syn[s].lemma_names[0]
            w2 = '***' + syn[s].lemma_names[0] + '*** (' + w + ')'
            textprint.append(w2)
        else:
            textprint.append(w)
            #print '---', w
    return ' '.join(textprint)

#print ' '.join(textprint)
#print main(doc)
