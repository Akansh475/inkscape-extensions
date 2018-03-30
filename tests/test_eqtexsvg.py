#!/usr/bin/env python

from tests.base import TestCase, test_support
from eqtexsvg import *

class EQTEXSVGBasicTest(TestCase):
    effect = EQTEXSVG

if __name__ == '__main__':
    test_support.run_unittest(EQTEXSVGBasicTest)
