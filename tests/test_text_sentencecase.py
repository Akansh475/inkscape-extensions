# coding=utf-8
from tests.base import InkscapeExtensionTestMixin, TestCase
from text_sentencecase import C


class TestSentenceCaseBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = C
        self.e = self.effect()
