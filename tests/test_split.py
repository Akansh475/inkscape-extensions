# coding=utf-8
from split import Split
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from inkex.tester.filters import CompareOrderIndependentTags

class TestSplitBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    """Test split effect"""
    effect_class = Split
    comparisons = [('--id=t1', '--id=t3')]
    compare_filters = [CompareOrderIndependentTags()]
