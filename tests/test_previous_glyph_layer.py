# coding=utf-8
from previous_glyph_layer import PreviousLayer
from tests.base import InkscapeExtensionTestMixin, TestCase

class TestPreviousLayerBasic(InkscapeExtensionTestMixin, TestCase):
    effect_class = PreviousLayer
