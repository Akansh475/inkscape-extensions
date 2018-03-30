#!/usr/bin/env python

from tests.base import TestCase, test_support
from interp_att_g import *

class InterpAttGBasicTest(TestCase):
    effect = InterpAttG

if __name__ == '__main__':
    test_support.run_unittest(InterpAttGBasicTest)
