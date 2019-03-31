# coding=utf-8
from pathalongpath import PathAlongPath
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.filters import CompareNumericFuzzy, CompareWithPathSpace

class TestPathAlongPathBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    compare_filters = [CompareNumericFuzzy(), CompareWithPathSpace()]
    comparisons = [('--copymode=Single', '--id=p1', '--id=p2')]
    effect_class = PathAlongPath
