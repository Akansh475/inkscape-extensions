# coding=utf-8
from dimension import Dimension
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase


class TestDimensionBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Dimension
        self.e = self.effect()
