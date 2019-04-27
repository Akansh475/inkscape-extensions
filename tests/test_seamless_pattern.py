# coding=utf-8
from seamless_pattern import C
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from inkex.tester.filters import CompareNumericFuzzy

class SeamlessPatternBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = C
    compare_filters = [CompareNumericFuzzy()]
