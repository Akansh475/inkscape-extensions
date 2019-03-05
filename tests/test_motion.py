# coding=utf-8
from motion import Motion
from tests.base import InkscapeExtensionTestMixin, TestCase


class MotionBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Motion
        self.e = self.effect()
