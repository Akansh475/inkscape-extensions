# coding=utf-8
from hpgl_input import HpglFile
from tests.base import InkscapeExtensionTestMixin, TestCase


class TestHpglFileBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = HpglFile
        self.e = self.effect()
