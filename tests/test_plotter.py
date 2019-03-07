# coding=utf-8
from plotter import Plot
from tests.base import InkscapeExtensionTestMixin, TestCase


class TestPlotBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Plot
        self.e = self.effect()
