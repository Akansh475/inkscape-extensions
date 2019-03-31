# coding=utf-8
from tests.base import InkscapeExtensionTestMixin, TestCase
from web_transmit_att import InkWebTransmitAtt


class TestInkWebTransmitAttBasic(InkscapeExtensionTestMixin, TestCase):
    effect_class = InkWebTransmitAtt
