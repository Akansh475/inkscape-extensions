# coding=utf-8
from hpgl_input import HpglFile
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class TestHpglFileBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect = HpglFile
    compare_file = 'ref_test.hpgl'
    comparisons = [()]
