# coding=utf-8
from dpiswitcher import DPISwitcher
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.filters import CompareNumericFuzzy

class TestDPISwitcherBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = DPISwitcher
    compare_filters = [CompareNumericFuzzy()]
