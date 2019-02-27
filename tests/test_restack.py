#!/usr/bin/env python
# coding=utf-8

import unittest

from restack import Restack
from tests.base import InkscapeExtensionTestMixin, TestCase


class RestackBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Restack
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
