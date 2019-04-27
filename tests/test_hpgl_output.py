# coding=utf-8
from hpgl_output import HpglOutput
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase


class HPGLOutputBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = HpglOutput
    comparisons = []
