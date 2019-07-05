# coding=utf-8
from text_split import Split
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class TestSplitBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    """Test split effect"""
    effect_class = Split
    comparisons = [('--id=t1', '--id=t3')]
