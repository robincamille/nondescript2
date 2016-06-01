# Specify the source of the training corpus here.
# Specify averages & frequencies from background corpus used on
# the output page.


backgroundcorpus = '/Volumes/ROBINDAVIS/Nondescript/train/'
#must be directory; include trailing slash

filelist = 'train_above280Kbytes.txt'
#list of files in background corpus directory to include in
#background corpus (you may want to exclude files under a
#certain word lenth, like 50k words)

topcorpuswords10000 = 'top10000.txt'
topcorpuswords1000 = 'top1000.txt'
topcorpuswords100 = 'top100.txt'
#lists of the top 10k, 1k, and 100 most frequent words
#in the background corpus.
#included file represents top words in the Blog Authorship
#Corpus from 2004.

bcfreqs = 'train_top1000_all-freqs_smoothed_avg_2col.csv'
#frequencies of vocab words across background corpus
#csv must be in this form: 'a',0.02345\n'able',0.00345\n...
#included file represents top words in the Blog Authorship
#Corpus from 2004.

minfreq = 0.0000000176
#float: frequency of a word that appears in the background corpus
#only one time. used to smooth comparison freqs on output page.

backgroundcorpusWL = 6.89168
#float: average word length from background corpus

backgroundcorpusSL = 104.33064
#float: average sentence length from background corpus
