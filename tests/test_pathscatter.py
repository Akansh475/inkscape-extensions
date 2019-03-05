# coding=utf-8
from pathscatter import PathScatter
from tests.base import InkscapeExtensionTestMixin, TestCase


class TestPathScatterBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = PathScatter
        self.e = self.effect()
