# coding=utf-8
from dots import Dots
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase


class DotsBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Dots
        self.e = self.effect()
