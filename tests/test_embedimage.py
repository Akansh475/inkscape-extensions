# coding=utf-8
from embedimage import Embedder
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase


class EmbedderBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = Embedder
