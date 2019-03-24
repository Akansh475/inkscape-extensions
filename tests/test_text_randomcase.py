# coding=utf-8
from tests.base import InkscapeExtensionTestMixin, TestCase
from text_randomcase import RandomCase


class TestRandomCaseBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = RandomCase
