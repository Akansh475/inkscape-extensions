# coding=utf-8
from extractimage import ExtractImage
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class ExtractImageBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect = ExtractImage
