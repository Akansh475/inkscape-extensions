# coding=utf-8
from lindenmayer import LSystem
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from inkex.tester.filters import CompareOrderIndependentStyle

class LSystemBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = LSystem
    compare_filters = [CompareOrderIndependentStyle()]
