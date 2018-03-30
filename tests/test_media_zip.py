#!/usr/bin/env python

from tests.base import TestCase, test_support
from media_zip import CompressedMediaOutput

class CompressedMediaOutputBasicTest(TestCase):
    effect = CompressedMediaOutput

if __name__ == '__main__':
    test_support.run_unittest(CompressedMediaOutputBasicTest)
