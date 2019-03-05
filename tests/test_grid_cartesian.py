# coding=utf-8
from grid_cartesian import GridCartesian
from tests.base import InkscapeExtensionTestMixin, TestCase


class GridPolarBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = GridCartesian
        self.e = self.effect()
