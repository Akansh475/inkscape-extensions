# coding=utf-8
from dots import Dots
from tests.base import InkscapeExtensionTestMixin, TestCase


class DotsBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Dots
        self.e = self.effect()
