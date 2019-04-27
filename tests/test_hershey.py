# coding=utf-8
from hershey import Hershey
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from inkex.tester.filters import CompareNumericFuzzy, CompareOrderIndependentStyle

class TestHersheyBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = Hershey
    comparisons = [('--fontface=timesr', )]
    compare_filters = [CompareNumericFuzzy(), CompareOrderIndependentStyle()]
