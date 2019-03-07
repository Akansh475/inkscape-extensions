# coding=utf-8
from hershey import Hershey
from tests.base import InkscapeExtensionTestMixin, TestCase


class TestHersheyBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Hershey
        self.e = self.effect()
