# coding=utf-8
from inkwebeffect import InkWebEffect
from tests.base import InkscapeExtensionTestMixin, TestCase


class InkWebEffectBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = InkWebEffect
        self.e = self.effect()
