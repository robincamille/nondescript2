# NondeScript 

This is my in-progress thesis work, spring 2016.

## Proposal 

NondeScript: Identifying and Disguising Writeprints

Every person has a writeprint, a unique, quantifiable writing style. This is at the heart of authorship attribution: a statistical analysis of multiple papers can very closely cluster those with the same authors. In the literature, authorship attribution and stylometry are often employed in cyberforensics and sometimes the humanities. But because the writeprint is a ‘behavioral biometric’ (Li et al. 2006), it also belongs to the realm of privacy. Just as we might keep our email password and browsing history private, we may sometimes want to keep our writing style private, too. For instance, a whistleblower may want to send an anonymous email from within an organization. Even though the technology used to transmit such a message might be totally sanitized of identifiable data, the writing itself may betray the author. Internet users are producing more and more textual content, effectively building an open corpus of their own writing, which could be used to unmask anonymous authors. The FBI already successfully uses stylometry to track down suspected criminals, particularly on the dark web (EFF 2010). However, as we have seen with documents revealed by Edward Snowden in 2013, some technologies meant for crime-fighting and war have been co-opted to spy on everyday citizens. This reveal prompted a public discussion of privacy and intense interest in digital privacy tools, from Tor to PGP to cookie-clearing. These widely available tools address every dependency in a line of communication except for the writeprint.  

I propose to build an auto-anonymizer, trained on corpora containing emails and other forms of digital communication, that disguises the author's writeprint. This will be accomplished by identifying the most “telling” features of the author’s writing (sentence length, bigrams, lexical density, and others) and lessening their effects. For instance, sentence length may be modified by splitting or joining sentences; synonyms may be found to increase or decrease reading level or syllable count; and so forth. The program will be evaluated by comparing before and after texts with several common classifiers, including those in Sci-Kit Learn. 

Rachel Greenstadt at Drexel University has pursued what she calls "adversarial stylometry" using the same tactic. Brennan and Greenstadt (2012) also found that machine translation is not a reliable way to mask identity, but automated attribution was much more difficult if an author tried to mask their style intentionally. Greenstadt’s research team released Anonymouth in 2012, a Java-based program that flags places where authors might manually change their writing to mask their identity. (The program is no longer under development.)

 

### Bibliography


* Artificial Intelligence Laboratory, University of Arizona. Dark Web and GeoPolitical Web Research. (n.d.). Retrieved February 1, 2016, from https://ai.arizona.edu/research/dark-web-geo-web

* Brennan, M. R., & Greenstadt, R. (2009). Practical Attacks Against Authorship Recognition Techniques. In Twenty-First IAAI Conference. Retrieved from http://www.aaai.org/ocs/index.php/IAAI/IAAI09/paper/view/257

* Brennan, M., Afroz, S., & Greenstadt, R. (2012). Adversarial Stylometry: Circumventing Authorship Recognition to Preserve Privacy and Anonymity. ACM Transactions on Information and System Security, 15(3). Retrieved from https://www.cs.drexel.edu/~sa499/papers/adversarial_stylometry.pdf

* Electronic Frontier Foundation. Government Uses Social Networking Sites for More than Investigations. (2010, August 16). Retrieved February 1, 2016, from https://www.eff.org/deeplinks/2010/08/government-monitors-much-more-social-networks

* Iqbal, F., Binsalleeh, H., Fung, B. C. M., & Debbabi, M. (2013). A unified data mining solution for authorship analysis in anonymous textual communications. Information Sciences, 231, 98–112. http://doi.org/10.1016/j.ins.2011.03.006

* Li, J., Zheng, R., & Chen, H. (2006). From fingerprint to writeprint. Communications of the ACM, 49(4), 76–82. http://doi.org/10.1145/1121949.1121951

* McDonald, A. W. E., Afroz, S., Caliskan, A., Stolerman, A., & Greenstadt, R. (2012). Use Fewer Instances of the Letter “i”: Toward Writing Style Anonymization. Privacy Enhancing Technologies: 12th International Symposium, PETS 2012, LNCS 7384. Retrieved from https://www.cs.drexel.edu/~sa499/papers/anonymouth.pdf

* Mining writeprints from anonymous e-mails for forensic investigation. (2009). Retrieved from http://dmas.lab.mcgill.ca/fung/pub/IBFD10di.pdf

* Murkute, A. M., & Gadge, J. (2015). Framework for user identification using writeprint approach. In 2015 International Conference on Technologies for Sustainable Development (ICTSD) (pp. 1–5). http://doi.org/10.1109/ICTSD.2015.7095924

* Schmid, M. R., Iqbal, F., & Fung, B. C. M. (2015). E-mail authorship attribution using customized associative classification. Digital Investigation, 14, S116–S126. http://doi.org/10.1016/j.diin.2015.05.012

* Schneier, B. Identifying People by their Writing Style. Schneier on Security. (n.d.). Retrieved February 1, 2016, from https://www.schneier.com/blog/archives/2011/08/identifying_peo_2.html

* Sheridan, M. (2014, June 29). Sex, drugs and videotape: the intrigue and allegations of bribery against GSK in China. The Sunday Times (London), p. 8.

* The Cyber Security and Information Systems Information Analysis Center (CSIAC). (n.d.). Retrieved February 1, 2016, from https://www.csiac.org/

