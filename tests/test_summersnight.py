#!/usr/bin/env python
#
# Revision history:
#  * 2012-01-28 (jazzynico): first working version (only checks the extension
#    with the default parameters).
#

import unittest

from summersnight import Project
from tests.base import InkscapeExtensionTestMixin, TestCase


class EnvelopeBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Project
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
