import chardataeffect
from text_uppercase import C
from tests.base import TestCase
import unittest
from helper_random_word import Word
import string

class UpperCase(TestCase):
	def setUp(self):
		self.e = C()
		self.w = Word()

	def test_lowercase(self):
		var = self.w.wordGenerator(15)
		var_new = var.lower()
		self.assertEqual(self.e.process_chardata(var_new), var.upper())

	def test_titlecase(self):
		var = self.w.wordGenerator(5)
		var1 = self.w.wordGenerator(8)
		var2 = self.w.wordGenerator(7)
		word = var + " " + var1 + " " + var2

		word_new = word.title()
		self.assertEqual(self.e.process_chardata(word_new), word_new.upper())

	def test_sentencecase(self):
		var = self.w.wordGenerator(5)
		var1 = self.w.wordGenerator(8)
		var2 = self.w.wordGenerator(7)
		word = var + " " + var1 + " " + var2

		word_new = word[0].upper() + word[1:]
		self.assertEqual(self.e.process_chardata(word_new), word_new.upper())
 

	def test_numbers_before(self):
		var = self.w.wordGenerator(15)
		var_new = var.zfill(20)
		self.assertEqual(self.e.process_chardata(var_new), var_new.upper())



	def test_punctuation_before(self):
		var = self.w.wordGenerator(15)
		var_new = string.punctuation + var
		self.assertEqual(self.e.process_chardata(var_new), var_new.upper())
	

if __name__ == '__main__':
    unittest.main()


