# coding=utf-8
from rubberstretch import RubberStretch
from tests.base import InkscapeExtensionTestMixin, TestCase


class TestRubberStretchBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = RubberStretch
        self.e = self.effect()
