#!/usr/bin/env python

from tests.base import TestCase
import unittest
from restack import *

class RestackBasicTest(TestCase):
    effect = Restack

if __name__ == '__main__':
    unittest.main()
