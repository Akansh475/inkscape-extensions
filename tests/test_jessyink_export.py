#!/usr/bin/en
# coding=utf-8

import unittest

from jessyInk_export import MyEffect
from tests.base import InkscapeExtensionTestMixin, TestCase


class JessyInkExportBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = MyEffect
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
