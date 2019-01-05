#!/usr/bin/env python

from tests.base import TestCase
import unittest
from hpgl_output import *

class HPGLOutputBasicTest(TestCase):
    effect = HpglOutput

if __name__ == '__main__':
    unittest.main()
