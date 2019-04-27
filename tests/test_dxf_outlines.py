# coding=utf-8
from dxf_outlines import DxfOutlines
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase


class DFXOutlineBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = DxfOutlines
