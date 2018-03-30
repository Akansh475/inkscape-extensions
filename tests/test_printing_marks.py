#!/usr/bin/env python

from tests.base import TestCase, test_support
from printing_marks import *

class PrintingMarksBasicTest(TestCase):
    effect = PrintingMarks

if __name__ == '__main__':
    test_support.run_unittest(PrintingMarksBasicTest)
