# coding=utf-8
from hpgl_input import HpglFile
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class TestHpglFileBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = HpglFile
    compare_file = 'io/test.hpgl'
    comparisons = [()]
