# coding=utf-8
from embedimage import Embedder
from tests.base import InkscapeExtensionTestMixin, TestCase


class EmbedderBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Embedder
        self.e = self.effect()