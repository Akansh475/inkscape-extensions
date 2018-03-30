#!/usr/bin/env python

from tests.base import TestCase, test_support
from straightseg import *

class SegmentStraightenerBasicTest(TestCase):
    effect = SegmentStraightener

if __name__ == '__main__':
    test_support.run_unittest(SegmentStraightenerBasicTest)
