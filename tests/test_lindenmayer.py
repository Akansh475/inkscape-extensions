# coding=utf-8
from lindenmayer import LSystem
from tests.base import InkscapeExtensionTestMixin, TestCase


class LSystemBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = LSystem
        self.e = self.effect()
