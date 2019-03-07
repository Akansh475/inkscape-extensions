# coding=utf-8
from layout_nup import Nup
from tests.base import InkscapeExtensionTestMixin, TestCase


class TestNupBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Nup
        self.e = self.effect()
