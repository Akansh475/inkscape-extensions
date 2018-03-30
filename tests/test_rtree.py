#!/usr/bin/env python

from tests.base import TestCase, test_support
from rtree import *

class RTreeTurtleBasicTest(TestCase):
    effect = RTreeTurtle

if __name__ == '__main__':
    test_support.run_unittest(RTreeTurtleBasicTest)
