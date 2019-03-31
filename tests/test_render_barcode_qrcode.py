# coding=utf-8
from render_barcode_qrcode import QRCodeInkscape
from tests.base import InkscapeExtensionTestMixin, TestCase

class TestQRCodeInkscapeBasic(InkscapeExtensionTestMixin, TestCase):
    effect_class = QRCodeInkscape
