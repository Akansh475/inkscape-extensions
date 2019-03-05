# coding=utf-8

from chardataeffect import CharDataEffect
from tests.base import InkscapeExtensionTestMixin, TestCase


class CharDataBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = CharDataEffect
        self.e = self.effect()
