#!/usr/bin/en
# coding=utf-8

import unittest

from jessyInk_summary import JessyInk_Summary
from tests.base import InkscapeExtensionTestMixin, TestCase


class JessyInkSummaryBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = JessyInk_Summary
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
