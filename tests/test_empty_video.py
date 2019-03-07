# coding=utf-8
from empty_video import EmptyVideo
from tests.base import InkscapeExtensionTestMixin, TestCase


class TestEmptyVideoBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = EmptyVideo
        self.e = self.effect()
