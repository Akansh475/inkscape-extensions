#!/usr/bin/env python
#
# Revision history:
#  * 2012-01-28 (jazzynico): first working version (only checks the extension
#    with the default parameters).
#

from unittest import TestCase
import unittest
from summersnight import Project

class EnvelopeBasicTest(TestCase):
    effect = Project

if __name__ == '__main__':
    unittest.main()
