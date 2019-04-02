# coding=utf-8
from voronoi2svg import Voronoi2svg
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.filters import CompareOrderIndependentStyle

class TestVoronoi2svgBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = Voronoi2svg
    compare_filters = [CompareOrderIndependentStyle()]
    comparisons = [('--id=p1', '--id=r3')]
