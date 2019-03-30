# coding=utf-8
from funcplot import FuncPlot
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.filters import CompareNumericFuzzy

class FuncPlotBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect = FuncPlot
    compare_filters = [CompareNumericFuzzy()]
