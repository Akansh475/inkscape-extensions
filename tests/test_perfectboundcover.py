#!/usr/bin/env python

from tests.base import TestCase
import unittest
from perfectboundcover import *

class PerfectBoundCoverBasicTest(TestCase):
    effect = PerfectBoundCover

if __name__ == '__main__':
    unittest.main()
