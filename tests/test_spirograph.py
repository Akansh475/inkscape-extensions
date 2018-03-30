#!/usr/bin/env python

from tests.base import TestCase, test_support
from spirograph import *

class SpirographBasicTest(TestCase):
    effect = Spirograph

if __name__ == '__main__':
    test_support.run_unittest(SpirographBasicTest)
