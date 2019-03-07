# coding=utf-8
from tests.base import InkscapeExtensionTestMixin, TestCase
from whirl import Whirl


class WhirlBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Whirl
        self.e = self.effect()
