#!/usr/bin/env python

from tests.base import TestCase
import unittest
from embedimage import *

class EmbedderBasicTest(TestCase):
    effect = Embedder

if __name__ == '__main__':
    unittest.main()
