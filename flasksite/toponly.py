# considers only the words in the top 9,989, 1000, or 100 most frequently used words in English

with open('top10000.txt') as top10kfile:
    top10kraw = top10kfile.readlines()
    top10k = [i[:-1] for i in top10kraw]

with open('top1000.txt') as top1kfile:
    top1kraw = top1kfile.readlines()
    top1k = [i[:-1] for i in top1kraw]

with open('top100.txt') as top100file:
    top100raw = top100file.readlines()
    top100 = [i[:-1] for i in top100raw]

def top(fulltext,howmany):
    """Returns a given text with only the words in the top 100, 1000, or 10,000 words in English."""
    if howmany == 10000:
        top = [w for w in fulltext.lower().split() if w in top10k]
        return ' '.join(top)
    if howmany == 1000:
        top = [w for w in fulltext.lower().split() if w in top1k]
        return ' '.join(top)
    if howmany == 100:
        top = [w for w in fulltext.lower().split() if w in top100]
        return ' '.join(top)

