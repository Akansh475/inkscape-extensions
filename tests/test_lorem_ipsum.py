# coding=utf-8
from lorem_ipsum import MyEffect
from tests.base import InkscapeExtensionTestMixin, TestCase


class MyEffectBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = MyEffect
        self.e = self.effect()
