#!/usr/bin/env python
# coding=utf-8

import unittest

from color_moresaturation import C
from tests.base import TestCase


class ColorMoreSaturationBasicTest(TestCase):
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
        self.assertEqual("c3bcbc", col)

    def test_default_values_grey(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Grey
        col = self.e.colmod(128, 128, 128)
        self.assertEqual("867979", col)

    def test_default_values_maroon(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Maroon
        col = self.e.colmod(128, 0, 0)
        self.assertEqual("800000", col)

    def test_default_values_red(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Red
        col = self.e.colmod(255, 0, 0)
        self.assertEqual("ff0000", col)

    def test_default_values_olive(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Olive
        col = self.e.colmod(128, 128, 0)
        self.assertEqual("808000", col)

    def test_default_values_yellow(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Yellow
        col = self.e.colmod(255, 255, 0)
        self.assertEqual("ffff00", col)

    def test_default_values_green(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Green
        col = self.e.colmod(0, 128, 0)
        self.assertEqual("008000", col)

    def test_default_values_lime(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Lime
        col = self.e.colmod(0, 255, 0)
        self.assertEqual("00ff00", col)

    def test_default_values_teal(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Teal
        col = self.e.colmod(0, 128, 128)
        self.assertEqual("008080", col)

    def test_default_values_aqua(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Aqua
        col = self.e.colmod(0, 255, 255)
        self.assertEqual("00ffff", col)

    def test_default_values_navy(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Navy
        col = self.e.colmod(0, 0, 128)
        self.assertEqual("000080", col)

    def test_default_values_blue(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Blue
        col = self.e.colmod(0, 0, 255)
        self.assertEqual("0000ff", col)

    def test_default_values_purple(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Purple
        col = self.e.colmod(128, 0, 128)
        self.assertEqual("800080", col)

    def test_default_values_fuschia(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Fuschia
        col = self.e.colmod(255, 0, 255)
        self.assertEqual("ff00ff", col)


if __name__ == '__main__':
    unittest.main()
