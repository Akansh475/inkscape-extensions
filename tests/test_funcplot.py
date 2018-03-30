#!/usr/bin/env python

from tests.base import TestCase, test_support
from funcplot import *

class FuncPlotBasicTest(TestCase):
    effect = FuncPlot

if __name__ == '__main__':
    test_support.run_unittest(FuncPlotBasicTest)
