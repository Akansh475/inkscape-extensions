#!/usr/bin/env python
# coding=utf-8

import unittest

from dxf_outlines import DxfOutlines
from tests.base import InkscapeExtensionTestMixin, TestCase


class DFXOutlineBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = DxfOutlines
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
