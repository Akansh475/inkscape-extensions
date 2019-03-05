# coding=utf-8
from fractalize import PathFractalize
from tests.base import InkscapeExtensionTestMixin, TestCase


class PathFractalizeBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = PathFractalize
        self.e = self.effect()
