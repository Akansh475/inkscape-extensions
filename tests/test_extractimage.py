#!/usr/bin/env python

from tests.base import TestCase, test_support
from extractimage import *

class ExtractImageBasicTest(TestCase):
    effect = MyEffect

if __name__ == '__main__':
    test_support.run_unittest(ExtractImageBasicTest)
