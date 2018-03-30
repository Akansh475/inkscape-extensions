#!/usr/bin/env python

from tests.base import TestCase, test_support
from render_alphabetsoup import *

class AlphabetSoupBasicTest(TestCase):
    effect = AlphabetSoup

if __name__ == '__main__':
    test_support.run_unittest(AlphabetSoupBasicTest)
