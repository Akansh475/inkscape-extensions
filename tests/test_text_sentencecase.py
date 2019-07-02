# coding=utf-8
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from text_sentencecase import SentanceCase

class TestSentenceCaseBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = SentanceCase
    comparisons = [()]
