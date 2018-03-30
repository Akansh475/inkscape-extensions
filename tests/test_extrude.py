#!/usr/bin/env python

from tests.base import TestCase, test_support
from extrude import *

class ExtrudeBasicTest(TestCase):
    effect = Extrude

if __name__ == '__main__':
    test_support.run_unittest(Extrude)
