# coding=utf-8
from tests.base import InkscapeExtensionTestMixin, TestCase
from text_randomcase import C


class TestRandomCaseBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = C
        self.e = self.effect()
