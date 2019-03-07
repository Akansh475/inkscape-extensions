#!/usr/bin/en
# coding=utf-8
from jessyInk_uninstall import JessyInk_Uninstall
from tests.base import InkscapeExtensionTestMixin, TestCase


class JessyInkUninstallBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = JessyInk_Uninstall
        self.e = self.effect()
