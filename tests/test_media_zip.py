# coding=utf-8
from media_zip import CompressedMediaOutput
from tests.base import InkscapeExtensionTestMixin, TestCase


class CompressedMediaOutputBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = CompressedMediaOutput
        self.e = self.effect()
