# coding=utf-8

from fig_input import FigInput

from tests.base import ComparisonMixin, TestCase

class TestFigInput(ComparisonMixin, TestCase):
    effect_class = FigInput
    compare_file = 'ref_test.fig'
    comparisons = [()]
