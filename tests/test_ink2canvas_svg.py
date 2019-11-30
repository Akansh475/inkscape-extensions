#!/usr/bin/en
# coding=utf-8
from ink2canvas import Ink2Canvas
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from inkex.tester.filters import CompareOrderIndependentLines

class Ink2CanvasBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = Ink2Canvas
    compare_filters = [CompareOrderIndependentLines()]
    comparisons = [()]
