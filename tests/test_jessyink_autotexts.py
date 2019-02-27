#!/usr/bin/en
# coding=utf-8

import unittest

from jessyInk_autoTexts import JessyInk_AutoTexts
from tests.base import InkscapeExtensionTestMixin, TestCase


class JessyInkAutoTextsBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = JessyInk_AutoTexts
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
