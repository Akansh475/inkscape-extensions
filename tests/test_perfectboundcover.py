# coding=utf-8
from perfectboundcover import PerfectBoundCover
from tests.base import InkscapeExtensionTestMixin, TestCase


class PerfectBoundCoverBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = PerfectBoundCover
        self.e = self.effect()
