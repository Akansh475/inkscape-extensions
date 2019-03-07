# coding=utf-8
from pathalongpath import PathAlongPath
from tests.base import InkscapeExtensionTestMixin, TestCase


class TestPathAlongPathBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = PathAlongPath
        self.e = self.effect()
