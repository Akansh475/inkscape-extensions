# coding=utf-8
from dots import Dots
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.filters import CompareOrderIndependentStyle

class DotsBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = Dots
    comparisons = [('--id=p1', '--id=r3')]
    compare_filters = [CompareOrderIndependentStyle()]
