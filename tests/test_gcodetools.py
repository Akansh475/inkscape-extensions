# coding=utf-8
from gcodetools import Gcodetools
from tests.base import InkscapeExtensionTestMixin, TestCase


class TestGcodetoolsBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Gcodetools
        self.e = self.effect()
