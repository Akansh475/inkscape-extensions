# coding=utf-8
from render_barcode_qrcode import QrCode
#from render_barcode_qrcode import QRCodeInkscape
from inkex.tester import ComparisonMixin, TestCase

class TestQRCodeInkscapeBasic(ComparisonMixin, TestCase):
    effect_class = QrCode
    #effect_class = QRCodeInkscape
