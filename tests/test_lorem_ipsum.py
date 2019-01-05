#!/usr/bin/env python

from tests.base import TestCase
import unittest
from lorem_ipsum import *

class MyEffectBasicTest(TestCase):
    effect = MyEffect

if __name__ == '__main__':
    unittest.main()
