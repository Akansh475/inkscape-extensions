# coding=utf-8
from tests.base import InkscapeExtensionTestMixin, TestCase
from text_flipcase import FlipCase


class TestFlipCaseBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = FlipCase
