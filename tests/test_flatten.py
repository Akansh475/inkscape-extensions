# coding=utf-8
from flatten import Flatten
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.filters import CompareNumericFuzzy, CompareWithPathSpace

class FlattenBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    compare_filters = [CompareNumericFuzzy(), CompareWithPathSpace()]
    effect_class = Flatten
