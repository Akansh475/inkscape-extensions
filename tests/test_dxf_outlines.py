# coding=utf-8
from dxf_outlines import DxfOutlines
from tests.base import InkscapeExtensionTestMixin, TestCase


class DFXOutlineBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = DxfOutlines
        self.e = self.effect()
