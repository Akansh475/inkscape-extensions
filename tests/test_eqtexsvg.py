# coding=utf-8
from eqtexsvg import EQTEXSVG
from tests.base import InkscapeExtensionTestMixin, TestCase


class EQTEXSVGBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = EQTEXSVG
        self.e = self.effect()
