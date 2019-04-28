# coding=utf-8
"""
Test inkex.cubic_paths
"""

from inkex import cubic_paths
from inkex.tester import TestCase


class CubicPathTest(TestCase):

    def assertDeepAlmostEqual(self, first, second, places=7, msg=None, delta=None):
        if isinstance(first, (list, tuple)):
            for (f, s) in zip(first, second):
                self.assertDeepAlmostEqual(f, s, places, msg, delta)
        else:
            self.assertAlmostEqual(first, second, places, msg, delta)

    def test_LHV(self):
        p = [
            ['M', [1.2, 2.3]],
            ['L', [3.4, 4.5]],
            ['H', [5.6]],
            ['V', [6.7]],
        ]
        csp = cubic_paths.CubicSuperPath(p)
        self.assertDeepAlmostEqual(csp, [[
            [[1.2, 2.3], [1.2, 2.3], [1.2, 2.3]],
            [[3.4, 4.5], [3.4, 4.5], [3.4, 4.5]],
            [[5.6, 4.5], [5.6, 4.5], [5.6, 4.5]],
            [[5.6, 6.7], [5.6, 6.7], [5.6, 6.7]],
        ]])

    def test_CS(self):
        p = [
            ['M', [1.2, 2.3]],
            ['C', [4.5, 3.4, 5.6, 6.7, 8.9, 7.8]],
            ['S', [9.1, 1.2, 2.3, 3.4]],
        ]
        csp = cubic_paths.CubicSuperPath(p)
        self.assertDeepAlmostEqual(csp, [[
            [[1.2, 2.3], [1.2, 2.3], [4.5, 3.4]],
            [[5.6, 6.7], [8.9, 7.8], [12.2, 8.9]],
            [[9.1, 1.2], [2.3, 3.4], [2.3, 3.4]],
        ]])

    def test_QT(self):
        p = [
            ['M', [0.0, 0.0]],
            ['Q', [3.0, 0.0, 3.0, 3.0]],
            ['T', [0.0, 6.0]],
        ]
        csp = cubic_paths.CubicSuperPath(p)
        self.assertDeepAlmostEqual(csp, [[
            [[0.0, 0.0], [0.0, 0.0], [2.0, 0.0]],
            [[3.0, 1.0], [3.0, 3.0], [3.0, 5.0]],
            [[2.0, 6.0], [0.0, 6.0], [0.0, 6.0]],
        ]])

    def test_AZ(self):
        p = [
            ['M', [0., 4.]],
            ['A', [3., 6., 0., 1, 1, 5., 4.]],
            ['Z', []],
        ]
        csp = cubic_paths.CubicSuperPath(p)
        self.assertTrue(len(csp[0]) > 3)

    def test_relative(self):
        # relative commands not implemented
        p = [
            ['M', [0.0, 0.0]],
            ['h', [1.0]],
        ]
        with self.assertRaises(ValueError):
            cubic_paths.CubicSuperPath(p)
