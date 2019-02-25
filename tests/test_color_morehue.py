#!/usr/bin/env python
# coding=utf-8

import unittest

from color_morehue import C
from tests.base import TestCase


class ColorMoreHueBasicTest(TestCase):
    def setUp(self):
        self.e = C()

    def test_default_values_black(self):
        args = [self.empty_svg]
        self.e.run(args)
        col = self.e.colmod(0, 0, 0)
        self.assertEqual("000000", col)

    def test_default_values_white(self):
        args = [self.empty_svg]
        self.e.run(args)
        col = self.e.colmod(255, 255, 255)
        self.assertEqual("ffffff", col)

    def test_default_values_silver(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Silver
        col = self.e.colmod(192, 192, 192)
        self.assertEqual("c0c0c0", col)

    def test_default_values_grey(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Grey
        col = self.e.colmod(128, 128, 128)
        self.assertEqual("808080", col)

    def test_default_values_maroon(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Maroon
        col = self.e.colmod(128, 0, 0)
        self.assertEqual("802600", col)

    def test_default_values_red(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Red
        col = self.e.colmod(255, 0, 0)
        self.assertEqual("ff4c00", col)

    def test_default_values_olive(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Olive
        col = self.e.colmod(128, 128, 0)
        self.assertEqual("598000", col)

    def test_default_values_yellow(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Yellow
        col = self.e.colmod(255, 255, 0)
        self.assertEqual("b2ff00", col)

    def test_default_values_green(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Green
        col = self.e.colmod(0, 128, 0)
        self.assertEqual("008026", col)

    def test_default_values_lime(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Lime
        col = self.e.colmod(0, 255, 0)
        self.assertEqual("00ff4c", col)

    def test_default_values_teal(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Teal
        col = self.e.colmod(0, 128, 128)
        self.assertEqual("005980", col)

    def test_default_values_aqua(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Aqua
        col = self.e.colmod(0, 255, 255)
        self.assertEqual("00b2ff", col)

    def test_default_values_navy(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Navy
        col = self.e.colmod(0, 0, 128)
        self.assertEqual("260080", col)

    def test_default_values_blue(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Blue
        col = self.e.colmod(0, 0, 255)
        self.assertEqual("4c00ff", col)

    def test_default_values_purple(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Purple
        col = self.e.colmod(128, 0, 128)
        self.assertEqual("800059", col)

    def test_default_values_fuschia(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Fuschia
        col = self.e.colmod(255, 0, 255)
        self.assertEqual("ff00b2", col)


if __name__ == '__main__':
    unittest.main()
