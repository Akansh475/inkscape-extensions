#!/usr/bin/env python

from tests.base import TestCase, test_support
from triangle import Triangle

class TriangleBasicTest(TestCase):
    effect = Triangle

if __name__ == '__main__':
    test_support.run_unittest(TriangleBasicTest)
