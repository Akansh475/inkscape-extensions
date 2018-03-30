#!/usr/bin/env python

from tests.base import TestCase, test_support
from handles import *

class HandlesBasicTest(TestCase):
    effect = Handles

if __name__ == '__main__':
    test_support.run_unittest(HandlesBasicTest)
