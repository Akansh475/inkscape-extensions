"""
The function wordGenerator generates a random word comprised of:

- lowercase letters
- uppercase letters
- digits
- punctuations

The function sentencecase takes a word that is generated
from wordGenerator($^&inkscape) and makes the first letter
uppercase.  

This is used for testing purposes for the text extensions


"""

import random
import string
import inkex

class Word(inkex.Effect):
    def wordGenerator(self, text_length):
        word = ""

        for i in range(0, text_length):
            word += random.choice(string.ascii_lowercase + \
            					  string.ascii_uppercase + \
            					  string.digits + \
            					  string.punctuation)

        return word

    def sentencecase(self, word):
        word_new = ""
        lower_letters = list(string.ascii_lowercase)
        first = True
        for letter in word:
            if letter in lower_letters and first == True:
                word_new += letter.upper()
                first = False
            else:
                word_new += letter

        return word_new



if __name__ == '__main__':
    e = Word()
    e.affect()
