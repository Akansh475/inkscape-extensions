# coding=utf-8
from previous_glyph_layer import PreviousLayer
from tests.base import InkscapeExtensionTestMixin, TestCase


class TestPreviousLayerBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = PreviousLayer
        self.e = self.effect()
