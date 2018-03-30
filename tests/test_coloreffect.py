#!/usr/bin/env python

from tests.base import TestCase, test_support
from coloreffect import *

class ColorEffectBasicTest(TestCase):
    effect = ColorEffect

if __name__ == '__main__':
    test_support.run_unittest(ColorEffectBasicTest)
