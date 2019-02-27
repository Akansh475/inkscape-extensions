#!/usr/bin/env python
# coding=utf-8

import unittest

from perfectboundcover import PerfectBoundCover
from tests.base import InkscapeExtensionTestMixin, TestCase


class PerfectBoundCoverBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = PerfectBoundCover
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
