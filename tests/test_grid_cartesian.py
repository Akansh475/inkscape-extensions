#!/usr/bin/env python

from tests.base import TestCase, test_support
from grid_cartesian import *

class GridPolarBasicTest(TestCase):
    effect = GridPolar

if __name__ == '__main__':
    test_support.run_unittest(GridPolarBasicTest)
