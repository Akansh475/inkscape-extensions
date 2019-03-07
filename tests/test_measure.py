# coding=utf-8
from measure import Length
from tests.base import InkscapeExtensionTestMixin, TestCase


class LengthBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Length
        self.e = self.effect()
