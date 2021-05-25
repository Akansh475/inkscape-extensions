# coding=utf-8
from render_barcode_qrcode import QrCode, QRCode
from inkex.tester import ComparisonMixin, TestCase

class TestQRCodeInkscapeBasic(ComparisonMixin, TestCase):
    """Test basic use of QR codes"""
    effect_class = QrCode
    compare_file = 'svg/empty.svg'
    comparisons = [
        ('--text=0123456789', '--typenumber=0', '--modulesize=10', '--drawtype=greedy'),
        ('--text=BreadRolls', '--typenumber=2', '--encoding=utf8', '--modulesize=10',
         '--drawtype=greedy'),
        ('--text=Blue Front Yard', '--typenumber=3', '--correctionlevel=1', '--modulesize=10',
         '--drawtype=greedy'),
        ('--text=Waterfall', '--typenumber=1', '--drawtype=circle', '--modulesize=10'),
        ('--text=groupid', '--groupid=testid', '--modulesize=10', '--drawtype=greedy'),
    ]

class TestQRCodeInkscapeSymbol(ComparisonMixin, TestCase):
    """Test symbols in qr codes"""
    effect_class = QrCode
    compare_file = 'svg/symbol.svg'
    comparisons = [
        ('--text=ThingOne', '--drawtype=symbol', '--correctionlevel=2',
         '--symbolid=AirTransportation_Inv', '--modulesize=10'),
    ]
