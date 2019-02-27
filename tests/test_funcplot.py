#!/usr/bin/env python
# coding=utf-8

import unittest

from funcplot import FuncPlot
from tests.base import InkscapeExtensionTestMixin, TestCase


class FuncPlotBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = FuncPlot
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
