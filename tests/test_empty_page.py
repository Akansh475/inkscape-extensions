# coding=utf-8
from empty_page import EmptyPage
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from inkex.tester.filters import CompareNumericFuzzy

class TestEmptyPageBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = EmptyPage
    compare_filters = [CompareNumericFuzzy()]
