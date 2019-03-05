# coding=utf-8
from extractimage import ExtractImage
from tests.base import InkscapeExtensionTestMixin, TestCase


class ExtractImageBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = ExtractImage
        self.e = self.effect()
