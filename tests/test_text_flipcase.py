# coding=utf-8
from tests.base import InkscapeExtensionTestMixin, TestCase
from text_flipcase import C


class TestFlipCaseBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = C
        self.e = self.effect()
