#!/usr/bin/env python

from tests.base import TestCase, test_support
from inkwebeffect import *

class InkWebEffectBasicTest(TestCase):
    effect = InkWebEffect

if __name__ == '__main__':
    test_support.run_unittest(InkWebEffectBasicTest)
