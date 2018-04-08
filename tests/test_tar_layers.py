#!/usr/bin/env python

from tests.base import TestCase, test_support
from tar_layers import LayersOutput

class LayersOutputBasicTest(TestCase):
    effect = LayersOutput

if __name__ == '__main__':
    test_support.run_unittest(LayersOutputBasicTest)
