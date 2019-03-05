# coding=utf-8
from render_barcode_qrcode import QRCodeInkscape
from tests.base import InkscapeExtensionTestMixin, TestCase


class TestQRCodeInkscapeBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = QRCodeInkscape
        self.e = self.effect()
