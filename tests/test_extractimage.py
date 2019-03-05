# coding=utf-8
from extractimage import MyEffect
from tests.base import InkscapeExtensionTestMixin, TestCase


class ExtractImageBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = MyEffect
        self.e = self.effect()
