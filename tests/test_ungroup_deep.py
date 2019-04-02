# coding=utf-8
from ungroup_deep import Ungroup
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.filters import CompareOrderIndependentStyle

class TestUngroupBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = Ungroup
    compare_filters = [CompareOrderIndependentStyle()]
