# coding=utf-8
from new_glyph_layer import NewGlyphLayer
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class TestNewGlyphLayerBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect = NewGlyphLayer
