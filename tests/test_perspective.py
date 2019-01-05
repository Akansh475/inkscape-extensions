#!/usr/bin/env python
#
# Unit test file for ../perspective.py
# Revision history:
#  * 2012-01-28 (jazzynico): first working version (only checks the extension
#    with the default parameters).
#

from tests.base import TestCase
import unittest
from perspective import *

class PerspectiveBasicTest(TestCase):
    effect = Project

if __name__ == '__main__':
    unittest.main()
