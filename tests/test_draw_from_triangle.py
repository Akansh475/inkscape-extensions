#!/usr/bin/env python

from tests.base import TestCase, test_support
from draw_from_triangle import *

class DrawFromTriangleBasicTest(TestCase):
    effect = Draw_From_Triangle

if __name__ == '__main__':
    test_support.run_unittest(DrawFromTriangleBasicTest)
