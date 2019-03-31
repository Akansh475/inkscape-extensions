# coding=utf-8
from hpgl_input import HpglFile
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class TestHpglFileBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = HpglFile
    compare_file = 'ref_test.hpgl'
    comparisons = [()]
