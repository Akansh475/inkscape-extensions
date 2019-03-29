# coding=utf-8
from dxf_outlines import DxfOutlines
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase


class DFXOutlineBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect = DxfOutlines

    def setUp(self):
        self.e = self.effect()
