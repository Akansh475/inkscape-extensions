# coding=utf-8
from coloreffect import ColorEffect
from inkex.tester import InkscapeExtensionTestMixin, TestCase

class ColorEffectBasicTest(InkscapeExtensionTestMixin, TestCase):
    effect_class = ColorEffect
