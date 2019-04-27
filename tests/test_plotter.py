# coding=utf-8
from plotter import Plot
from inkex.tester import InkscapeExtensionTestMixin, TestCase

class TestPlotBasic(InkscapeExtensionTestMixin, TestCase):
    effect_class = Plot
