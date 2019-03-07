# coding=utf-8
from render_alphabetsoup import AlphabetSoup
from tests.base import InkscapeExtensionTestMixin, TestCase


class AlphabetSoupBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = AlphabetSoup
        self.e = self.effect()
