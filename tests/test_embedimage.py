# coding=utf-8
from embedimage import Embedder
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase


class EmbedderBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect = Embedder
    def setUp(self):
        self.e = self.effect()
