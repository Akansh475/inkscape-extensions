#!/usr/bin/env python
# coding=utf-8

import unittest

from jitternodes import JitterNodes
from tests.base import InkscapeExtensionTestMixin, TestCase


class JitterNodesBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = JitterNodes
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
