# coding=utf-8
from layers2svgfont import Layers2SVGFont
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class TestLayers2SVGFontBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = Layers2SVGFont
