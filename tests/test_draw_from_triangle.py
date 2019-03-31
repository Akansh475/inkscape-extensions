# coding=utf-8
from draw_from_triangle import DrawFromTriangle
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class DrawFromTriangleBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = DrawFromTriangle
