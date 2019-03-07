# coding=utf-8
from image_attributes import SetAttrImage
from tests.base import InkscapeExtensionTestMixin, TestCase


class TestSetAttrImageBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = SetAttrImage
        self.e = self.effect()
