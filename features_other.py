def lowertext(text):
    """Returns a text in all lowercase"""
    lowtext = []
    text = text.split()
    for w in text:
        w = w.lower()
        lowtext.append(w) 
    return lowtext

def avgwordlength(text):
    """Returns average word length in a text (float)"""
    lowtext = lowertext(text)  
    textfreq = getfreq(lowtext)
    words = textfreq.keys() #dedupe for slightly better results
    totalchars = 0
    for s in words: #may include some punctuation
        totalchars = totalchars + len(s)
    textlength = len(words)
    return totalchars / float(textlength)

def avgsentlength(text):
    """Returns average sentence length in a text, in chars (float)"""
    textstring = ' '.join(text)
    sents = sentsplitter.tokenize(textstring)
    totalsentlength = 0
    for s in sents:
        totalsentlength = totalsentlength + len(s) #length in chars
    numsents = len(sents)
    return totalsentlength / float(numsents)
