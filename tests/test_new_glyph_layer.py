# coding=utf-8
from new_glyph_layer import NewGlyphLayer
from tests.base import InkscapeExtensionTestMixin, TestCase


class TestNewGlyphLayerBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = NewGlyphLayer
        self.e = self.effect()
