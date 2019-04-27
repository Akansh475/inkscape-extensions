# coding=utf-8
from empty_dvd_cover import DvdCover
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from inkex.tester.filters import CompareNumericFuzzy

class TestDvdCoverBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = DvdCover
    compare_filters = [CompareNumericFuzzy()]
    comparisons = [('-s', '10', '-b', '10')]
