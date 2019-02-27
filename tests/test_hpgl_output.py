#!/usr/bin/env python
# coding=utf-8

import unittest

from hpgl_output import HpglOutput
from tests.base import InkscapeExtensionTestMixin, TestCase


class HPGLOutputBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = HpglOutput
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
