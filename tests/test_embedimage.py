# coding=utf-8
from embedimage import Embedder
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class EmbedderBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = Embedder
    compare_file = 'svg/images.svg'
    comparisons = (
        (),
    )
