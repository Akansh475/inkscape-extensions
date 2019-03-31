# coding=utf-8
from nicechart import NiceChart
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class TestNiceChartBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect = NiceChart
