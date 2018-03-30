#!/usr/bin/env python

from tests.base import TestCase, test_support
from guides_creator import *

class GuidesCreatorBasicTest(TestCase):
    effect = GuidesCreator

if __name__ == '__main__':
    test_support.run_unittest(GuidesCreatorBasicTest)
