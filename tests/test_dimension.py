# coding=utf-8
from dimension import Dimension
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase


class TestDimensionBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = Dimension
