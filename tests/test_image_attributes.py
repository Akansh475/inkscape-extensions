# coding=utf-8
from image_attributes import SetAttrImage
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class TestSetAttrImageBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = SetAttrImage
