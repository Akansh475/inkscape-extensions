#!/usr/bin/env python

from tests.base import TestCase
import unittest
from tar_layers import LayersOutput

class LayersOutputBasicTest(TestCase):
    effect = LayersOutput

if __name__ == '__main__':
    unittest.main()
