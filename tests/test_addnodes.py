#!/usr/bin/en

from tests.base import TestCase, test_support
from addnodes import *

class SplitItBasicTest(TestCase):
    effect = SplitIt

if __name__ == '__main__':
    test_support.run_unittest(SplitItBasicTest)
