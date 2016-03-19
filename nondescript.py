# Adds words and phrases to text to anonymize

from random import randint

phrases = ['I think', 'It seems to me', 'You know', 'If you know what I mean', \
           'Like', 'However', 'So be it', 'It is what it is', 'Really', \
           'To wit', 'Obviously', 'To tell you the truth', 'Trust me', \
           'Damn it', 'Seriously', 'Literally', 'What an opportunity', \
           'You see']
           
def main(text):
    i = 0
    while i < 20:
        addphrase = phrases[randint(0,len(phrases)-1)] + ' '
        text = text + ' ' + addphrase
        i += 1
    return text
