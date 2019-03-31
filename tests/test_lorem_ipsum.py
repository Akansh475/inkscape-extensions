# coding=utf-8
from lorem_ipsum import MyEffect
from tests.base import InkscapeExtensionTestMixin, TestCase

class MyEffectBasicTest(InkscapeExtensionTestMixin, TestCase):
    effect_class = MyEffect
