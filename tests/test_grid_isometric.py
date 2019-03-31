# coding=utf-8

from grid_isometric import GridIsometric
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.filters import CompareOrderIndependentStyle

class TestGridIsometricBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    compare_filters = [CompareOrderIndependentStyle()]
    effect_class = GridIsometric
