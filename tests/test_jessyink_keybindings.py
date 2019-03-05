#!/usr/bin/en
# coding=utf-8
from jessyInk_keyBindings import JessyInk_CustomKeyBindings
from tests.base import InkscapeExtensionTestMixin, TestCase


class JessyInkCustomKeyBindingsBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = JessyInk_CustomKeyBindings
        self.e = self.effect()
