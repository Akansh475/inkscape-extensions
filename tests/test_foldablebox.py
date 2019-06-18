# coding=utf-8
from foldablebox import FoldableBox
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from inkex.tester.filters import CompareOrderIndependentStyle

class FoldableBoxArguments(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = FoldableBox
    compare_filters = [CompareOrderIndependentStyle()]
