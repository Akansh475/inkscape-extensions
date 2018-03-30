#!/usr/bin/env python

from tests.base import TestCase, test_support
from embedimage import *

class EmbedderBasicTest(TestCase):
    effect = Embedder

if __name__ == '__main__':
    test_support.run_unittest(EmbedderBasicTest)
