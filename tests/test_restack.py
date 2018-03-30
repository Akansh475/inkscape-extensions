#!/usr/bin/env python

from tests.base import TestCase, test_support
from restack import *

class RestackBasicTest(TestCase):
    effect = Restack

if __name__ == '__main__':
    test_support.run_unittest(RestackBasicTest)
