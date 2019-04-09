# coding=utf-8
from pathscatter import PathScatter
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.filters import CompareWithoutIds

class TestPathScatterBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = PathScatter
    comparisons = [('--id=p1', '--id=r3'),]
    compare_filters = [CompareWithoutIds()]
