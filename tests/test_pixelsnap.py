# coding=utf-8
from pixelsnap import PixelSnapEffect
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.fitlers import CompareOrderIndependentStyle

class TestPixelSnapEffectBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = PixelSnapEffect
    compare_filters = [CompareOrderIndependentStyle()]
