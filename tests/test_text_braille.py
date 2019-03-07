# coding=utf-8
from tests.base import InkscapeExtensionTestMixin, TestCase
from text_braille import C


class TestBrailleBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = C
        self.e = self.effect()
