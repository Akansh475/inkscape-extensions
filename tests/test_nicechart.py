# coding=utf-8
from nicechart import NiceChart
from tests.base import InkscapeExtensionTestMixin, TestCase


class TestNiceChartBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = NiceChart
        self.e = self.effect()
