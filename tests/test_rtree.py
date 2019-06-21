# coding=utf-8
from rtree import RTreeTurtle
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from inkex.tester.filters import CompareNumericFuzzy

class RTreeTurtleBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = RTreeTurtle
    comparisons = [()]
    compare_filters = [CompareNumericFuzzy(),]
