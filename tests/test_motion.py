#!/usr/bin/env python

from tests.base import TestCase, test_support
from motion import *

class MotionBasicTest(TestCase):
    effect = Motion

if __name__ == '__main__':
    test_support.run_unittest(MotionBasicTest)
