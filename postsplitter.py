# Split Blog Authorship Corpus XML files into subfiles by post
# Create labels .txt file for each [filename] [sourcefilename]

# To run from command line:
# python postsplitter.py [source data directory] [destination data directory] [name to give labels, e.g. test]

import re, os, sys

#for all files in dir...
datadir = sys.argv[1]
outdir = sys.argv[2] + '/' #eg "blogtrain/blogtrainsplit/"
name = sys.argv[3]

#create labels
labelfilename = name + "_labels.txt"
labelfile = open(labelfilename,'w')
labels = []

for ffile in os.listdir(datadir):
    if ffile.endswith(".xml"):
        sourcefile = ffile[:-4]
        #print sourcefile

        #open file
        filename = open(datadir + "/" + ffile,'r')
        data = filename.read()
        filename.close()

        #create new files for each post
        datas = data.split("<date>") #break up post
        c = 0
        for i in datas[1:]: #first is Blog title

            pattern = re.compile('.*?<\/date>') 
            match = re.search(pattern,i)
            skip = len(match.group(0)) + 8 #length of date plus <post>
            body = i[skip:-11] #until </post>
            
            outfilename = outdir + sourcefile + str(c) + ".txt"
            outfile = open(outfilename,'w')
            outfile.write(body)
            outfile.close()

            label = sourcefile + str(c) + ".txt," + sourcefile
            labels.append(label)
            c += 1

for l in labels:
    labelfile.write(l)
    labelfile.write('\n')

labelfile.close()
    
print 'Done'
