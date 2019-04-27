# coding=utf-8
from dpiswitcher import DPISwitcher
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from inkex.tester.filters import CompareNumericFuzzy

class TestDPISwitcherBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = DPISwitcher
    compare_filters = [CompareNumericFuzzy()]
