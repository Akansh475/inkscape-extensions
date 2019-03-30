# coding=utf-8
from grid_cartesian import GridCartesian
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.filters import CompareOrderIndependentStyle

class GridPolarBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect = GridCartesian
    compare_filters = [CompareOrderIndependentStyle()]
