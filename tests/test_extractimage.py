# coding=utf-8
from extractimage import ExtractImage
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class ExtractImageBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = ExtractImage
