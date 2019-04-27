# coding=utf-8
from web_transmit_att import InkWebTransmitAtt
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class TestInkWebTransmitAttBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = InkWebTransmitAtt
    comparisons = [('--id=p1', '--id=r3')]
