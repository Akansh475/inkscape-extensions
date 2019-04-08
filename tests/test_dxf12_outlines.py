# coding=utf-8
from dxf12_outlines import DxfTwelve
from tests.base import InkscapeExtensionTestMixin, TestCase


class TestDXF12OutlinesBasic(InkscapeExtensionTestMixin, TestCase):
    effect_class = DxfTwelve
