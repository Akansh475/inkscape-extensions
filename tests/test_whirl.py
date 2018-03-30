#!/usr/bin/env python

from tests.base import TestCase, test_support
from whirl import *

class WhirlBasicTest(TestCase):
    effect = Whirl

if __name__ == '__main__':
    test_support.run_unittest(WhirlBasicTest)
