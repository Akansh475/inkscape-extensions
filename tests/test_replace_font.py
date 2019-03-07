# coding=utf-8
from replace_font import ReplaceFont
from tests.base import InkscapeExtensionTestMixin, TestCase


class TestReplaceFontBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = ReplaceFont
        self.e = self.effect()
