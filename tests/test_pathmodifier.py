#!/usr/bin/env python

from tests.base import TestCase, test_support
from pathmodifier import *

class PathModifierBasicTest(TestCase):
    effect = PathModifier

if __name__ == '__main__':
    test_support.run_unittest(PathModifierBasicTest)
