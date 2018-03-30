#!/usr/bin/env python

from tests.base import TestCase, test_support
from perfectboundcover import *

class PerfectBoundCoverBasicTest(TestCase):
    effect = PerfectBoundCover

if __name__ == '__main__':
    test_support.run_unittest(PerfectBoundCoverBasicTest)
