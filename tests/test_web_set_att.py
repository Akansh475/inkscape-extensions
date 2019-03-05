# coding=utf-8
from tests.base import InkscapeExtensionTestMixin, TestCase
from web_set_att import InkWebTransmitAtt


class TestWebSetAttBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = InkWebTransmitAtt
        self.e = self.effect()
