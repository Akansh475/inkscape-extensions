# coding=utf-8
from restack import Restack
from tests.base import InkscapeExtensionTestMixin, TestCase


class RestackBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Restack
        self.e = self.effect()
