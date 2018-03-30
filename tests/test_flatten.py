#!/usr/bin/env python

from tests.base import TestCase, test_support
from flatten import *

class MyEffectBasicTest(TestCase):
    effect = MyEffect

if __name__ == '__main__':
    test_support.run_unittest(MyEffectBasicTest)
