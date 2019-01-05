import chardataeffect
from text_titlecase import TitleCase
from tests.base import TestCase
import unittest
from helper_random_word import Word
import string

class TitleCaseTest(TestCase):
	def setUp(self):
		self.title = TitleCase()
		self.word = Word()

	def test_lowercase(self):
		var = self.word.wordGenerator(6)
		var1 = self.word.wordGenerator(9)
		var2 = self.word.wordGenerator(10)
		words = var.lower() + " " + var1.lower() + " " + var2.lower()
		titlecase = self.title.process_chardata(words, True, True)
		self.assertEqual(self.title.process_chardata(words, True, True), titlecase)


	def test_uppercase(self):
		var = self.word.wordGenerator(6)
		var1 = self.word.wordGenerator(9)
		var2 = self.word.wordGenerator(10)
		words = var.upper() + " " + var1.upper() + " " + var2.upper()
		titlecase = self.title.process_chardata(words, True, True)
		self.assertEqual(self.title.process_chardata(words, True, True), titlecase)

	def test_sentencecase(self):
		var = self.word.wordGenerator(5)
		var1 = self.word.wordGenerator(8)
		var2 = self.word.wordGenerator(7)
		words = var + " " + var1 + " " + var2
		word_new = self.word.sentencecase(words)
		titlecase = self.title.process_chardata(word_new, True, True)
		self.assertEqual(self.title.process_chardata(word_new, True, True), titlecase)
 

	def test_numbers_before(self):
		words = self.word.wordGenerator(15)
		word_new = words.zfill(20)
		titlecase = self.title.process_chardata(word_new, True, True)
		self.assertEqual(self.title.process_chardata(word_new, True, True), titlecase)


	def test_punctuation_before(self):
		words = self.word.wordGenerator(15)
		word_new = string.punctuation + words
		titlecase = self.title.process_chardata(word_new, True, True)
		self.assertEqual(self.title.process_chardata(word_new, True, True), titlecase)
	
	def test_check_strings(self):
		titlecase_strings = [("i love inkscape", "I Love Inkscape"), 
		 					 ("i LOVE inkscape", "I Love Inkscape"),
		 					 ("I love Inkscape", "I Love Inkscape"),
		 					 ("I LOVE INKSCAPE", "I Love Inkscape"),
		 					 ("ThIs Is VeRy AwEsOmE", "This Is Very Awesome"),
		 					 ("!$this is Very awesome.", "!$This Is Very Awesome."),
		 					 ("this *is @very ^awesome.", "This *Is @Very ^Awesome."),
		 					 ("there is a      space.", "There Is A      Space."),
		 					 ("9these 5are 7numbers", "9These 5Are 7Numbers"),
		 					 ("thisworddidnotend", "Thisworddidnotend"),
		 					 ("This Should Not Change", "This Should Not Change")]

	
		for item in titlecase_strings:
			self.assertEqual(self.title.process_chardata(item[0], True, True), item[1])



if __name__ == '__main__':
    unittest.main()