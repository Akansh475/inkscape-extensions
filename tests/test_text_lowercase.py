"""
Test the lowercase effect
"""

import string

from text_lowercase import C

from .base import TestCase
from .base.word import word_generator

class LowerCase(TestCase):
    def setUp(self):
        #print("Setup")
        self.e = C()

    def test_uppercase(self):
        var = word_generator(15)
        #print("This is the word ", var)
        var_new = var.upper()
        #print("this is upper ", var_new)
        #print(">>>Testing all uppercase")
        #print("this is new var ", self.e.process_chardata(var))
        self.assertEqual(self.e.process_chardata(var_new), var.lower())

    def test_lowercase(self):
        var = word_generator(15)
        #print("This is the word ", var)
        var_new = var.lower()
        #print("this is lower ", var_new)
        #print(">>>Testing all lowercase")
        #print("this is new var ", self.e.process_chardata(var))
        self.assertEqual(self.e.process_chardata(var_new), var.lower())



    def test_titlecase(self):
        var = word_generator(5)
        var1 = word_generator(8)
        var2 = word_generator(7)
        word = var + " " + var1 + " " + var2

        #print("This is the word ", word)
        word_new = word.title()
        #print("this is title case ", word_new)
        #print(">>>Testing titlecase")
        #print("this is new var ", self.e.process_chardata(var))
        self.assertEqual(self.e.process_chardata(word_new), word_new.lower())

    def test_sentencecase(self):
        var = word_generator(5)
        var1 = word_generator(8)
        var2 = word_generator(7)
        word = var + " " + var1 + " " + var2

        #print("This is the word ", word)
        word_new = word[0].upper() + word[1:]
        #print("this is sentencecase ", word_new)
        #print(">>>Testing sentencecase")
        #print("this is new var ", self.e.process_chardata(var))
        self.assertEqual(self.e.process_chardata(word_new), word_new.lower())


    def test_numbers_before(self):
        var = word_generator(15)
        var_upper = var.upper()
        var_new = var_upper.zfill(20)
        #print("This is the word ", var_new)
        #print(">>>Testing numbers before ")
        #print("this is new var ", self.e.process_chardata(var))
        self.assertEqual(self.e.process_chardata(var_new), var_new.lower())


    def test_punctuation_before(self):
        var = word_generator(15)
        var_upper = var.upper()
        var_new = string.punctuation + var_upper
        #print("This is the word ", var_new)
        #print(">>>Testing punctuation before ")
        #print("this is new var ", self.e.process_chardata(var))
        self.assertEqual(self.e.process_chardata(var_new), var_new.lower())
