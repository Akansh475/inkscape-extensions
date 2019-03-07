# coding=utf-8
from draw_from_triangle import Draw_From_Triangle
from tests.base import InkscapeExtensionTestMixin, TestCase


class DrawFromTriangleBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Draw_From_Triangle
        self.e = self.effect()
