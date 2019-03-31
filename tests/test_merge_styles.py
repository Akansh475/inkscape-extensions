# coding=utf-8
from merge_styles import MergeStyles
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.filters import CompareOrderIndependentLines

class TestMergeStylesBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect = MergeStyles
    comparisons = [('--id=r3', '--id=c3')]
    compare_filters = [CompareOrderIndependentLines()]
