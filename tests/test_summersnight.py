#!/usr/bin/env python
#
# Revision history:
#  * 2012-01-28 (jazzynico): first working version (only checks the extension
#    with the default parameters).
#

from tests.base import TestCase, test_support
from summersnight import Project

class EnvelopeBasicTest(TestCase):
    effect = Project

if __name__ == '__main__':
    test_support.run_unittest(EnvelopeBasicTest)
