# coding=utf-8
from empty_desktop import EmptyDesktop
from tests.base import InkscapeExtensionTestMixin, TestCase


class TestEmptyDesktopBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = EmptyDesktop
        self.e = self.effect()
