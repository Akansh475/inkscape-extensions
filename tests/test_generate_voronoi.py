# coding=utf-8
from generate_voronoi import PatternEffect
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from inkex.tester.filters import CompareOrderIndependentStyle

class TestPatternBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = PatternEffect
    comparisons = [('--id=r3', '--id=p1'),]
    compare_filters = [CompareOrderIndependentStyle()]
