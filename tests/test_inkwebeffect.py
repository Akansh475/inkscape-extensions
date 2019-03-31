# coding=utf-8
from inkwebeffect import InkWebEffect
from tests.base import InkscapeExtensionTestMixin, TestCase


class InkWebEffectBasicTest(InkscapeExtensionTestMixin, TestCase):
    effect_class = InkWebEffect
