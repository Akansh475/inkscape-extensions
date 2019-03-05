# coding=utf-8
from svgfont2layers import SVGFont2Layers
from tests.base import InkscapeExtensionTestMixin, TestCase


class TestSVGFont2LayersBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = SVGFont2Layers
        self.e = self.effect()
