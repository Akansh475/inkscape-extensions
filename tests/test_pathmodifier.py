# coding=utf-8
from pathmodifier import PathModifier
from tests.base import InkscapeExtensionTestMixin, TestCase


class PathModifierBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = PathModifier
        self.e = self.effect()
