# coding=utf-8
from coloreffect import ColorEffect
from tests.base import InkscapeExtensionTestMixin, TestCase


class ColorEffectBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = ColorEffect
        self.e = self.effect()
