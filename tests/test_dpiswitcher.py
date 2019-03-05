# coding=utf-8
from dpiswitcher import DPISwitcher
from tests.base import InkscapeExtensionTestMixin, TestCase


class TestDPISwitcherBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = DPISwitcher
        self.e = self.effect()
