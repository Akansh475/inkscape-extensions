# coding=utf-8
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.filters import CompareNumericFuzzy, CompareWithPathSpace

from whirl import Whirl

class WhirlBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = Whirl
    compare_filters = [CompareNumericFuzzy(), CompareWithPathSpace()]
