# coding=utf-8
from dxf_input import DxfInput
from tests.base import InkscapeExtensionTestMixin, TestCase


class TestDxfInputBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = DxfInput
        self.e = self.effect()
