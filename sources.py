# Specify the source of the background corpus here, along with
# other data files specific to the background corpus.



backgroundcorpus = '/Volumes/ROBINDAVIS/Thesis_LocalAir/corpora/train_above280kb/'
#Must be a directory of plain-text files.
#Include the trailing slash.
#No sample corpus included with this package.
#Recommended: Blog Authorship Corpus from 2004.

filelist = '/Users/robindavis/Desktop/nondescript/blogtrainlist.txt'
#List of plain-text files in background corpus directory to include in
#background corpus. (You may want to exclude files under a
#certain word length, like 50k words.)
#File must be in this format: Filename.xml\nFilename.xml\n...
#Plaintext files can be .xml or .txt
#Included file represents top words in the Blog Authorship
#Corpus from 2004.

topcorpuswords10000 = 'data/top10000.txt'
topcorpuswords5000 = 'data/top5000_plus-punct.txt'
#topcorpuswords1000 = 'data/top1000.txt'
topcorpuswords1000 = 'data/top1000_plus-punct.txt'
topcorpuswords100 = 'data/top100.txt'
#Lists of the top 10k, 1k, and 100 most frequent words
#in the background corpus.
#File must be in this format: a\nthe\ni\n...
#Included files represent top words in the Blog Authorship
#Corpus from 2004.

bcfreqs = 'data/vocabulary_freqs.csv'
#Frequencies of vocab words across background corpus.
#CSV must be in this format: 'a',0.02345\n'able',0.00345\n...
#including single quotes around each word.
#Included file represents top words in the Blog Authorship
#Corpus from 2004.


# Averages & frequencies from background corpus used on
# the output page:

minfreq = 0.000000017
#Frequency of a word that appears in the background corpus
#only one time. Used to smooth comparison freqs on output page.
#Must be a float.

backgroundcorpusWL = 6.89
#Average word length from background corpus. Must be a float.

backgroundcorpusSL = 104.33
#Average sentence length from background corpus. Must be a float.
