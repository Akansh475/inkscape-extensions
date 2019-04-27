# coding=utf-8
from render_barcode_qrcode import QRCodeInkscape
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class TestQRCodeInkscapeBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = QRCodeInkscape
