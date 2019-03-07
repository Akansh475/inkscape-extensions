# coding=utf-8
from empty_icon import EmptyIcon
from tests.base import InkscapeExtensionTestMixin, TestCase


class TestEmptyIconBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = EmptyIcon
        self.e = self.effect()
