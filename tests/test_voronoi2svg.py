# coding=utf-8
from tests.base import InkscapeExtensionTestMixin, TestCase
from voronoi2svg import Voronoi2svg


class TestVoronoi2svgBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Voronoi2svg
        self.e = self.effect()
