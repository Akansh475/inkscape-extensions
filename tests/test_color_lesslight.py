#!/usr/bin/env python
# coding=utf-8

import unittest

from color_lesslight import C
from tests.base import InkscapeExtensionTestMixin, TestCase


class ColorLessLightBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = C
        self.e = self.effect()

    def test_default_values_black(self):
        args = [self.empty_svg]
        self.e.run(args)
        col = self.e.colmod(0, 0, 0)
        self.assertEqual("000000", col)

    def test_default_values_white(self):
        args = [self.empty_svg]
        self.e.run(args)
        col = self.e.colmod(255, 255, 255)
        self.assertEqual("f2f2f2", col)

    def test_default_values_silver(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Silver
        col = self.e.colmod(192, 192, 192)
        self.assertEqual("b3b3b3", col)

    def test_default_values_grey(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Grey
        col = self.e.colmod(128, 128, 128)
        self.assertEqual("737373", col)

    def test_default_values_maroon(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Maroon
        col = self.e.colmod(128, 0, 0)
        self.assertEqual("660000", col)

    def test_default_values_red(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Red
        col = self.e.colmod(255, 0, 0)
        self.assertEqual("e50000", col)

    def test_default_values_olive(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Olive
        col = self.e.colmod(128, 128, 0)
        self.assertEqual("666600", col)

    def test_default_values_yellow(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Yellow
        col = self.e.colmod(255, 255, 0)
        self.assertEqual("e5e500", col)

    def test_default_values_green(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Green
        col = self.e.colmod(0, 128, 0)
        self.assertEqual("006600", col)

    def test_default_values_lime(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Lime
        col = self.e.colmod(0, 255, 0)
        self.assertEqual("00e500", col)

    def test_default_values_teal(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Teal
        col = self.e.colmod(0, 128, 128)
        self.assertEqual("006666", col)

    def test_default_values_aqua(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Aqua
        col = self.e.colmod(0, 255, 255)
        self.assertEqual("00e5e5", col)

    def test_default_values_navy(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Navy
        col = self.e.colmod(0, 0, 128)
        self.assertEqual("000066", col)

    def test_default_values_blue(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Blue
        col = self.e.colmod(0, 0, 255)
        self.assertEqual("0000e5", col)

    def test_default_values_purple(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Purple
        col = self.e.colmod(128, 0, 128)
        self.assertEqual("660066", col)

    def test_default_values_fuschia(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Fuschia
        col = self.e.colmod(255, 0, 255)
        self.assertEqual("e500e5", col)


if __name__ == '__main__':
    unittest.main()
