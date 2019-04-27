# coding=utf-8
from funcplot import FuncPlot
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from inkex.tester.filters import CompareNumericFuzzy

class FuncPlotBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = FuncPlot
    compare_filters = [CompareNumericFuzzy()]
