#!/usr/bin/en
# coding=utf-8

import unittest

from addnodes import SplitIt
from tests.base import InkscapeExtensionTestMixin, TestCase


class SplitItBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = SplitIt
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
