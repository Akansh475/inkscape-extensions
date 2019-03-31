# coding=utf-8
from next_glyph_layer import NextLayer
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class TestNextLayerBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = NextLayer
