# coding=utf-8
from interp import Interp
from tests.base import InkscapeExtensionTestMixin, TestCase


class InterpBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Interp
        self.e = self.effect()
