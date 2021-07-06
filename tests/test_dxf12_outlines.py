# coding=utf-8
from dxf12_outlines import DxfTwelve
from inkex.tester import ComparisonMixin, TestCase


class TestDXF12OutlinesBasic(ComparisonMixin, TestCase):
    compare_file = ["svg/shapes.svg", "svg/preserved-transforms.svg",
                    "svg/dxf_nested_transforms.svg"]
    comparisons = [()]
    effect_class = DxfTwelve