#!/usr/bin/env python
# coding=utf-8

import unittest

from eqtexsvg import EQTEXSVG
from tests.base import InkscapeExtensionTestMixin, TestCase


class EQTEXSVGBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = EQTEXSVG
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
