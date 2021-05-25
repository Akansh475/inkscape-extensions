# coding=utf-8
from inkex.tester import ComparisonMixin, TestCase
from text_extract import Extract

class TestExtractBasic(ComparisonMixin, TestCase):
    effect_class = Extract
    stderr_output = True
    comparisons = [
        ('--direction=tb', '--xanchor=center_x', '--yanchor=center_y'),
        ('--direction=bt', '--xanchor=center_x', '--yanchor=center_y'),
        ('--direction=lr', '--xanchor=center_x', '--yanchor=center_y'),
        ('--direction=rl', '--xanchor=center_x', '--yanchor=center_y'),
    ]
