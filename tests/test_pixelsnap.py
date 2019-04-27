# coding=utf-8
from pixelsnap import PixelSnapEffect
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from inkex.tester.filters import CompareOrderIndependentStyle

class TestPixelSnapEffectBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = PixelSnapEffect
    compare_filters = [CompareOrderIndependentStyle()]
