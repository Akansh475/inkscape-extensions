# coding=utf-8
from lindenmayer import LSystem
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.filters import CompareOrderIndependentStyle

class LSystemBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect = LSystem
    compare_filters = [CompareOrderIndependentStyle()]
