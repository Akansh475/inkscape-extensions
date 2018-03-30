#!/usr/bin/env python

from tests.base import TestCase, test_support
from chardataeffect import *

class CharDataBasicTest(TestCase):
    effect = CharDataEffect

if __name__ == '__main__':
    test_support.run_unittest(CharDataBasicTest)
