#!/usr/bin/env python

from tests.base import TestCase, test_support
from edge3d import *

class Edge3dBasicTest(TestCase):
    effect = Edge3d

if __name__ == '__main__':
    test_support.run_unittest(Edge3dBasicTest)
