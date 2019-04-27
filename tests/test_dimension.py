# coding=utf-8
from dimension import Dimension
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class TestDimensionBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = Dimension
    comparisons = [('--id=p1', '--id=r3')]
