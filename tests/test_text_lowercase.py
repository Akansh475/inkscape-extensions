
import chardataeffect
from text_lowercase import C
from tests.base import TestCase, test_support
from helper_random_word import Word
import string

class LowerCase(TestCase):
	def setUp(self):
		#print("Setup")
		self.e = C()
		self.w = Word()


	def test_uppercase(self):
		var = self.w.wordGenerator(15)
		#print("This is the word ", var)
		var_new = var.upper()
		#print("this is upper ", var_new)
		#print(">>>Testing all uppercase")
		#print("this is new var ", self.e.process_chardata(var))
		self.assertEqual(self.e.process_chardata(var_new), var.lower())

	def test_lowercase(self):
		var = self.w.wordGenerator(15)
		#print("This is the word ", var)
		var_new = var.lower()
		#print("this is lower ", var_new)
		#print(">>>Testing all lowercase")
		#print("this is new var ", self.e.process_chardata(var))
		self.assertEqual(self.e.process_chardata(var_new), var.lower())



	def test_titlecase(self):
		var = self.w.wordGenerator(5)
		var1 = self.w.wordGenerator(8)
		var2 = self.w.wordGenerator(7)
		word = var + " " + var1 + " " + var2

		#print("This is the word ", word)
		word_new = word.title()
		#print("this is title case ", word_new)
		#print(">>>Testing titlecase")
		#print("this is new var ", self.e.process_chardata(var))
		self.assertEqual(self.e.process_chardata(word_new), word_new.lower())

	def test_sentencecase(self):
		var = self.w.wordGenerator(5)
		var1 = self.w.wordGenerator(8)
		var2 = self.w.wordGenerator(7)
		word = var + " " + var1 + " " + var2

		#print("This is the word ", word)
		word_new = word[0].upper() + word[1:]
		#print("this is sentencecase ", word_new)
		#print(">>>Testing sentencecase")
		#print("this is new var ", self.e.process_chardata(var))
		self.assertEqual(self.e.process_chardata(word_new), word_new.lower())


	def test_numbers_before(self):
		var = self.w.wordGenerator(15)
		var_upper = var.upper()
		var_new = var_upper.zfill(20)
		#print("This is the word ", var_new)
		#print(">>>Testing numbers before ")
		#print("this is new var ", self.e.process_chardata(var))
		self.assertEqual(self.e.process_chardata(var_new), var_new.lower())


	def test_punctuation_before(self):
		var = self.w.wordGenerator(15)
		var_upper = var.upper()
		var_new = string.punctuation + var_upper
		#print("This is the word ", var_new)
		#print(">>>Testing punctuation before ")
		#print("this is new var ", self.e.process_chardata(var))
		self.assertEqual(self.e.process_chardata(var_new), var_new.lower())
	



if __name__ == '__main__':
    test_support.run_unittest(LowerCase)



