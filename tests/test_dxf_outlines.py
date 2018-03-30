#!/usr/bin/env python

from tests.base import TestCase, test_support
from dxf_outlines import *

class DFXOutlineBasicTest(TestCase):
    effect = MyEffect

if __name__ == '__main__':
    test_support.run_unittest(DFXOutlineBasicTest)

