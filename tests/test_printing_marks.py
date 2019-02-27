#!/usr/bin/env python
# coding=utf-8

import unittest

from printing_marks import PrintingMarks
from tests.base import InkscapeExtensionTestMixin, TestCase


class PrintingMarksBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = PrintingMarks
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
