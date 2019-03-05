# coding=utf-8
from grid_isometric import GridPolar
from tests.base import InkscapeExtensionTestMixin, TestCase


class TestGridPolarBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = GridPolar
        self.e = self.effect()
