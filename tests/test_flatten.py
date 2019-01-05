#!/usr/bin/env python

from tests.base import TestCase
import unittest
from flatten import *

class MyEffectBasicTest(TestCase):
    effect = MyEffect

if __name__ == '__main__':
    unittest.main()
