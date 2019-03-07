# coding=utf-8
from tar_layers import LayersOutput
from tests.base import InkscapeExtensionTestMixin, TestCase


class LayersOutputBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = LayersOutput
        self.e = self.effect()
