# coding=utf-8
from nicechart import NiceChart
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class TestNiceChartBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = NiceChart
