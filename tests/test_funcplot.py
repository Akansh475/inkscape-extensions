# coding=utf-8
from funcplot import FuncPlot
from tests.base import InkscapeExtensionTestMixin, TestCase


class FuncPlotBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = FuncPlot
        self.e = self.effect()
