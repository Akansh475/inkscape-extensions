#!/usr/bin/env python

from tests.base import TestCase, test_support
from polyhedron_3d import *

class Poly3DBasicTest(TestCase):
    effect = Poly3D

if __name__ == '__main__':
    test_support.run_unittest(Poly3DBasicTest)
