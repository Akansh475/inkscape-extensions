# coding=utf-8
from rtree import RTreeTurtle
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class RTreeTurtleBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = RTreeTurtle
    comparisons = [()]
