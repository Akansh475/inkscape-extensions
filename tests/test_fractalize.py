#!/usr/bin/env python

from tests.base import TestCase, test_support
from fractalize import *

class PathFractalizeBasicTest(TestCase):
    effect = PathFractalize

if __name__ == '__main__':
    test_support.run_unittest(PathFractalizeBasicTest)
