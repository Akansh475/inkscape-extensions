# coding=utf-8
from pixelsnap import PixelSnapEffect
from tests.base import InkscapeExtensionTestMixin, TestCase


class TestPixelSnapEffectBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = PixelSnapEffect
        self.e = self.effect()
