# coding=utf-8
from dimension import Dimension
from tests.base import InkscapeExtensionTestMixin, TestCase


class TestDimensionBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Dimension
        self.e = self.effect()
