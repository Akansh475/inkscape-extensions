# coding=utf-8
from render_barcode_datamatrix import DataMatrix
from tests.base import InkscapeExtensionTestMixin, TestCase


class TestDataMatrixBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = DataMatrix
        self.e = self.effect()
