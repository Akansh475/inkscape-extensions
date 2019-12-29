# coding=utf-8
from hpgl_output import HpglOutput
from inkex.tester import ComparisonMixin, TestCase

class HPGLOutputBasicTest(ComparisonMixin, TestCase):
    effect_class = HpglOutput
