# coding=utf-8
from tests.base import InkscapeExtensionTestMixin, TestCase
from text_sentencecase import SentanceCase

class TestSentenceCaseBasic(InkscapeExtensionTestMixin, TestCase):
    effect_class = SentanceCase
