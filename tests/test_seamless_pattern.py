# coding=utf-8
from seamless_pattern import C
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.filters import CompareNumericFuzzy

class SeamlessPatternBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = C
    compare_filters = [CompareNumericFuzzy()]
