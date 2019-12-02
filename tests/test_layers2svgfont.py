# coding=utf-8
from layers2svgfont import LayersToSvgFont
from inkex.tester import ComparisonMixin, TestCase

class TestLayers2SVGFontBasic(ComparisonMixin, TestCase):
    effect_class = LayersToSvgFont
