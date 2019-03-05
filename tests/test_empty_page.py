# coding=utf-8
from empty_page import EmptyPage
from tests.base import InkscapeExtensionTestMixin, TestCase


class TestEmptyPageBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = EmptyPage
        self.e = self.effect()
