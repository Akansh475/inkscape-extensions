# coding=utf-8
from grid_polar import GridPolar
from tests.base import InkscapeExtensionTestMixin, TestCase


class GridPolarBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = GridPolar
        self.e = self.effect()
