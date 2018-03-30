#!/usr/bin/env python

from tests.base import TestCase, test_support
from dots import *

class DotsBasicTest(TestCase):
    effect = Dots

if __name__ == '__main__':
    test_support.run_unittest(DotsBasicTest)
