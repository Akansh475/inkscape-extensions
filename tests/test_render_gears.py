#!/usr/bin/env python

from tests.base import TestCase, test_support
from render_gears import *

class GearsBasicTest(TestCase):
    effect = Gears

if __name__ == '__main__':
    test_support.run_unittest(GearsBasicTest)
