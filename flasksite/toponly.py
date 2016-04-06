# considers only the words in the top 9,989 used words in English


infile = open('top10000.txt','r')
top10kraw = infile.readlines()
infile.close()
top10k = []
for i in top10kraw:
    top10k.append(i[:-1]) #ignore \n

def top(fulltext):
    top = []
    for word in fulltext.split():
        if word.lower() in top10k:
            top.append(word)
        else:
            pass
    return ' '.join(top)
