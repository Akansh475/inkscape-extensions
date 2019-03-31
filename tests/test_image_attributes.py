# coding=utf-8
from image_attributes import SetAttrImage
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class TestSetAttrImageBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = SetAttrImage
