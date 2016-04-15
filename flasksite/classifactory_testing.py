from classifactory import classifydocs

doc = open('compare-doc.txt','r')
docraw = doc.read()
doc.close()

msg = open('message-doc_anond.txt','r')
message = msg.read()
msg.close()

j = 0
while j < 5:
    printclassify = [i for i in classifydocs('/Users/robin/Documents/Thesis_local/corpora/blogs/train/',\
                                                 'train_above280Kbytes.txt',\
                                                 docraw,\
                                                 message,\
                                                 #anonmessage,\
                                                 10000)]
    for i in printclassify:
        print i
    print '==========================================================='
    j += 1
