# coding=utf-8

from grid_isometric import GridIsometric
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from inkex.tester.filters import CompareOrderIndependentStyle

class TestGridIsometricBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    compare_filters = [CompareOrderIndependentStyle()]
    effect_class = GridIsometric
