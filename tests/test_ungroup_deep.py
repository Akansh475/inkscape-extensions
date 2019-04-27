# coding=utf-8
from ungroup_deep import Ungroup
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from inkex.tester.filters import CompareOrderIndependentStyle

class TestUngroupBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = Ungroup
    compare_filters = [CompareOrderIndependentStyle()]
