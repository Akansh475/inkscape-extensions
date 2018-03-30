#!/usr/bin/env python

from tests.base import TestCase, test_support
from lindenmayer import *

class LSystemBasicTest(TestCase):
    effect = LSystem

if __name__ == '__main__':
    test_support.run_unittest(LSystemBasicTest)
