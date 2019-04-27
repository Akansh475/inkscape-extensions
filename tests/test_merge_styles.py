# coding=utf-8
from merge_styles import MergeStyles
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from inkex.tester.filters import CompareOrderIndependentLines

class TestMergeStylesBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = MergeStyles
    comparisons = [('--id=r3', '--id=c3')]
    compare_filters = [CompareOrderIndependentLines()]
