# coding=utf-8
from spirograph import Spirograph
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.filters import CompareOrderIndependentStyle

class SpirographBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = Spirograph
    compare_filters = [CompareOrderIndependentStyle()]
