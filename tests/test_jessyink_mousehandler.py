#!/usr/bin/en
# coding=utf-8

import unittest

from jessyInk_mouseHandler import JessyInk_CustomMouseHandler
from tests.base import InkscapeExtensionTestMixin, TestCase


class JessyInkCustomMouseHandlerBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = JessyInk_CustomMouseHandler
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
