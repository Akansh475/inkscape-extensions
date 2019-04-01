# coding=utf-8
from split import Split
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.filters import CompareOrderIndependentTags

class TestSplitBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = Split
    comparisons = [('--id=t1', '--id=t3')]
    compare_filters = [CompareOrderIndependentTags()]
