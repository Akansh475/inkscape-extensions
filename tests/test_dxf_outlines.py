#!/usr/bin/env python

from tests.base import TestCase, test_support
from dxf_outlines import DxfOutlines

class DFXOutlineBasicTest(TestCase):
    effect = DxfOutlines

if __name__ == '__main__':
    test_support.run_unittest(DFXOutlineBasicTest)

