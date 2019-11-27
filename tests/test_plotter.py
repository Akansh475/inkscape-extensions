# coding=utf-8
from plotter import Plot
from inkex.tester import ComparisonMixin, TestCase

class TestPlotBasic(ComparisonMixin, TestCase):
    stderr_output = True
    effect_class = Plot
    comparisons = [
        ('--serialPort=[test]',), # HPGL
        ('--serialPort=[test]', '--commandLanguage=DMPL'),
        ('--serialPort=[test]', '--commandLanguage=KNK'),
    ]
