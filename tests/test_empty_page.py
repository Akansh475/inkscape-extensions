# coding=utf-8
from empty_page import EmptyPage
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.filters import CompareNumericFuzzy

class TestEmptyPageBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect = EmptyPage
    compare_filters = [CompareNumericFuzzy()]
