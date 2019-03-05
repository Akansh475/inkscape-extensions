# coding=utf-8
from split import Split
from tests.base import InkscapeExtensionTestMixin, TestCase


class TestSplitBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Split
        self.e = self.effect()
