# coding=utf-8
from layers2svgfont import Layers2SVGFont
from tests.base import InkscapeExtensionTestMixin, TestCase


class TestLayers2SVGFontBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Layers2SVGFont
        self.e = self.effect()
