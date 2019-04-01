# coding=utf-8
from render_barcode_qrcode import QRCodeInkscape
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class TestQRCodeInkscapeBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = QRCodeInkscape
