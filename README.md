# Nondescript 

Work toward a computational linguistics thesis submitted spring 2016 by Robin Davis (robincamilledavis@gmail.com).
=======
This is my **very much in-progress** thesis work, spring 2016. Final code repo expected June 2016.

## Thesis

Davis, Robin Camille (2016). [*Nondescript: A Web Tool to Aid Subversion of Authorship Attribution* (master's thesis)](http://academicworks.cuny.edu/gc_etds/1343/). Graduate Center, City University of New York, New York.

(Completed for the [Computational Linguistics MA program](http://www.gc.cuny.edu/Page-Elements/Academics-Research-Centers-Initiatives/Doctoral-Programs/Linguistics/About-the-Program/Specializations/Computational-Linguistics).)

## About 

![Screenshot of input and output screens](http://robincamille.com/thesis/screenshot_all.jpg "Screenshots of Nondescript in the browser")

**Abstract:** A person’s writing style is uniquely quantifiable and can serve reliably as a biometric. A writer who wishes to remain anonymous can use a number of privacy technologies but can still be identified simply by the words they choose to use — how often they use the words "of" and "and," for instance. Nondescript is a web tool designed first to identify the user’s writing style (in terms of word frequency) from a given writing sample and message, then guide the author to make iterative changes to their message to lessen its probability of being attributed to them. While Nondescript does not guarantee anonymity, the web tool provides a user with an iterative interface to revise their writing and see results of a simulated authorship attribution scenario. Nondescript also provides a synonym-replacement feature, which significantly lowers the probability that a document will be attributed to the original author. 

**More info:** Nondescript uses Flask to generate the web interface. Input your writing sample and the message you wish to anonymize. Every time you run Nondescript, it randomly chooses 7 authors from a given background corpus to compare your writing to. This can take up to 60 seconds. (What's it doing during this time? In machine learning terms, every time you run Nondescript, it trains a Naive Bayes classifier on your sample and some writing by the 7 random authors, *then* runs the trained classifier on your message and other writings from the 7 random authors.) On the next page, you'll see if Nondescript was able to correctly attribute your message to you, or if you were able to confuse it into thinking it was written by someone else. At the bottom of the page, you'll have another chance to revise your message. 

You may get a different result every time you use Nondescript, even if you don't change your message. That's because this is a simulation of de-anonymization. In a real scenario, you may not know whose writing your anonymous message is being compared to. 

Future work on this project will include a user study and a dedicated interactive website that runs Nondescript. 

Questions? robincamilledavis@gmail.com (Please no code nitpicking.) 

 
## Download & use

Requires these libraries: sklearn, nltk, wordfilter, numpy, flask, more_itertools

Requires a background corpus structured as a directory that contains at least 20 plain-text files, each containing at least 50,000 words. (I recommend the [Blog Authorship Corpus](http://u.cs.biu.ac.il/~koppel/BlogCorpus.htm) from 2004.)

1. Download all required libraries using pip: sklearn, nltk, wordfilter, numpy, flask, more_itertools.
1. Open **sources.py**. Fill in the path of your background corpus. 
1. Create data files to reflect your background corpus, as specified in sources.py.
1. Run **compareform.py**. This fires up Flask. Head to http://127.0.0.1:5000/ in your browser to use the web-based interface. 

Main files:
- **compareform.py** gen


Released under a Creative Commons BY-NC license (attribute all uses to me and do not use for commercial purposes). Please cite my thesis. 
 