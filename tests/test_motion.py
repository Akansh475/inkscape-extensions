#!/usr/bin/env python
# coding=utf-8

import unittest

from motion import Motion
from tests.base import InkscapeExtensionTestMixin, TestCase


class MotionBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Motion
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
