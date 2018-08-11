"""
This function generates a random word comprised of:

- lowercase letters
- uppercase letters
- digits
- punctuations

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



if __name__ == '__main__':
    e = Word()
    e.affect()
