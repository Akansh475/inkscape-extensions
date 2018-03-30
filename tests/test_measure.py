#!/usr/bin/env python

from tests.base import TestCase, test_support
from measure import *

class LengthBasicTest(TestCase):
    effect = Length

if __name__ == '__main__':
    test_support.run_unittest(LengthBasicTest)
