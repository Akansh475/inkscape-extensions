# coding=utf-8
from empty_dvd_cover import DvdCover
from tests.base import InkscapeExtensionTestMixin, TestCase


class TestDvdCoverBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = DvdCover
        self.e = self.effect()
