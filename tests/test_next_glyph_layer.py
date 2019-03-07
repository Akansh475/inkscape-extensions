# coding=utf-8
from next_glyph_layer import NextLayer
from tests.base import InkscapeExtensionTestMixin, TestCase


class TestNextLayerBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = NextLayer
        self.e = self.effect()
