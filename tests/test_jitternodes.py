#!/usr/bin/env python

from tests.base import TestCase, test_support
from jitternodes import *

class JitterNodesBasicTest(TestCase):
    effect = JitterNodes

if __name__ == '__main__':
    test_support.run_unittest(JitterNodesBasicTest)
