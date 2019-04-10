# coding=utf-8
from generate_voronoi import PatternEffect
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.filters import CompareOrderIndependentStyle

class TestPatternBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = PatternEffect
    comparisons = [('--id=r3', '--id=p1'),]
    compare_filters = [CompareOrderIndependentStyle()]
