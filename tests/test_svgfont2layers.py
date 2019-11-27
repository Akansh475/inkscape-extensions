# coding=utf-8
from svgfont2layers import SVGFont2Layers
from inkex.tester import ComparisonMixin, TestCase

class TestSVGFont2LayersBasic(ComparisonMixin, TestCase):
    effect_class = SVGFont2Layers
    compare_file = 'svg/font.svg'
    comparisons = [
        ('--count=3',)
    ]
