# coding=utf-8
from render_barcode_datamatrix import DataMatrix
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class TestDataMatrixBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = DataMatrix
