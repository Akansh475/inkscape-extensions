# coding=utf-8
from plotter import Plot
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class TestPlotBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = Plot
