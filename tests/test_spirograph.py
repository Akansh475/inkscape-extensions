# coding=utf-8
from spirograph import Spirograph
from tests.base import InkscapeExtensionTestMixin, TestCase


class SpirographBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Spirograph
        self.e = self.effect()
