# coding=utf-8
from grid_cartesian import GridCartesian
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.filters import CompareOrderIndependentStyle

class GridCartesianBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = GridCartesian
    compare_filters = [CompareOrderIndependentStyle()]
