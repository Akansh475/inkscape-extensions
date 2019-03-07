#!/usr/bin/en
# coding=utf-8
from jessyInk_install import JessyInk_Install
from tests.base import InkscapeExtensionTestMixin, TestCase


class JessyInkInstallBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = JessyInk_Install
        self.e = self.effect()
