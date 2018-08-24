import chardataeffect
from text_titlecase import C
from tests.base import TestCase, test_support
from helper_random_word import Word
import string

class Titlecase(TestCase):
	def setUp(self):
		self.e = C()
		self.w = Word()

	def test_lowercase(self):
		var = self.w.wordGenerator(6)
		var1 = self.w.wordGenerator(9)
		var2 = self.w.wordGenerator(10)
		word = var.lower() + " " + var1.lower() + " " + var2.lower()
		titlecase = self.e.process_chardata(word, True, True)
		self.assertEqual(self.e.process_chardata(word, True, True), titlecase)


	def test_uppercase(self):
		var = self.w.wordGenerator(6)
		var1 = self.w.wordGenerator(9)
		var2 = self.w.wordGenerator(10)
		word = var.upper() + " " + var1.upper() + " " + var2.upper()
		titlecase = self.e.process_chardata(word, True, True)
		self.assertEqual(self.e.process_chardata(word, True, True), titlecase)

	def test_sentencecase(self):
		var = self.w.wordGenerator(5)
		var1 = self.w.wordGenerator(8)
		var2 = self.w.wordGenerator(7)
		word = var + " " + var1 + " " + var2
		word_new = self.w.sentencecase(word)
		titlecase = self.e.process_chardata(word_new, True, True)
		self.assertEqual(self.e.process_chardata(word_new, True, True), titlecase)
 

	def test_numbers_before(self):
		word = self.w.wordGenerator(15)
		word_new = word.zfill(20)
		titlecase = self.e.process_chardata(word_new, True, True)
		self.assertEqual(self.e.process_chardata(word_new, True, True), titlecase)


	def test_punctuation_before(self):
		word = self.w.wordGenerator(15)
		word_new = string.punctuation + word
		titlecase = self.e.process_chardata(word_new, True, True)
		self.assertEqual(self.e.process_chardata(word_new, True, True), titlecase)
	


if __name__ == '__main__':
    test_support.run_unittest(Titlecase)