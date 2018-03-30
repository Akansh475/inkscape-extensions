#!/usr/bin/env python

from tests.base import TestCase, test_support
from hpgl_output import *

class HPGLOuputBasicTest(TestCase):
    effect = HpglOutput

if __name__ == '__main__':
    test_support.run_unittest(HPGLOuputBasicTest)
