# coding=utf-8
from guillotine import Guillotine
from tests.base import InkscapeExtensionTestMixin, TestCase


class TestGuillotineBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Guillotine
        self.e = self.effect()
