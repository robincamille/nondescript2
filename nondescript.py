# Adds words and phrases to text to anonymize

from random import randint
from nltk.corpus import wordnet as wn
from nltk import word_tokenize as tok
##from nltk.stem.porter import PorterStemmer
##ps = PorterStemmer()



filename = open('blogtrain/890034.female.23.indUnk.Scorpio41.txt','r')
doc = filename.read()
filename.close()
text = tok(doc)
##
##doc2f = open('testdoc1b.txt','r')
##doc2 = doc2f.read()
##doc2f.close()

##doc2non = open('testdoc1b_nondescripted.txt','w')

##phrases = ['I think', 'It seems to me', 'You know', 'If you know what I mean', \
##           'Like', 'However', 'So be it', 'It is what it is', 'Really', \
##           'To wit', 'Obviously', 'To tell you the truth', 'Trust me', \
##           'Damn it', 'Seriously', 'Literally', 'What an opportunity', \
##           'You see']
           
#def changewords(text):
text = doc
##i = 0
text = text.split()
##    while i < 3:
##        addphrase = phrases[randint(0,len(phrases)-1)] + ' '
##        text.append(addphrase)
##        i += 1
textprint = []
c = 0
for w in text: #https://pythonism.wordpress.com/2013/10/07/simple-synonym-replacement/
    #print w
    w = w.lower()
    syn = wn.synsets(w)
    if len(w) < 3:
        textprint.append(w)
    elif 2 < len(syn) < 8:
        w2 = w
        #s = len(syn)-1
        s = 0
        wlist = []
##        while (w2 == w) or (s < len(syn)-1):
##            w2 = syn[s].lemma_names[0]
##            s += 1
##            wlist.append(w2)
        while w2.lower() == w:
            i = randint(0,len(syn)-1)
            w2 = syn[i].lemma_names[0]
            s += 1
            wlist.append(w2)
            if s == len(syn)-1:
                break
        #textprint.append((w2.upper()+ ' (' + w + ')'))
        textprint.append(('\n' + w2.upper() + ' ' + str(wlist) + ' (' + w + ')'))
        c += 1
    else:
        textprint.append(w)
        #print '---', w
#return ' '.join(textprint)

print ' '.join(textprint)
#print changewords(doc)

##doc2non.write(main(doc2))
##
##doc2non.close()
