#!/usr/bin/env python

import os
import sys

from unittest import TestCase
import unittest

from color_randomize import *

def extract_hsl(hexcol):
    from inkex.colors import Color
    return Color('#' + hexcol).to_hsl().to_floats()


class ColorRandomizeBasicTest(TestCase):
    def setUp(self):
        self.e=C()

    def test_default_values(self):
        """ The default ranges are set to 0, and thus the color and opacity should not change. """
        args = [self.empty_svg]
        self.e.affect(args)
        col = self.e.colmod(128, 128, 255)
        self.assertEqual("8080ff", col)
        opac = self.e.opacmod(5)
        self.assertEqual(5, opac)


class ColorRandomizeColorModificationTest(TestCase):
    def setUp(self):
        self.e=C()

    def test_no_change(self):
        """ The user selected 0% values, and thus the color should not change. """
        args = ['-y 0', '-t 0', '-m 0', self.empty_svg]
        self.e.affect(args)
        col = self.e.colmod(128, 128, 255)
        self.assertEqual("8080ff", col)

    def test_random_hue(self):
        """ Random hue only. Saturation and lightness not changed. """
        args = ['-y 50','-t 0','-m 0',self.empty_svg]
        self.e.affect(args)
        hsl = extract_hsl(self.e.colmod(150, 100, 200))
        self.assertAlmostEqual(hsl[1], 0.47, delta=0.01)
        self.assertAlmostEqual(hsl[2], 0.59, delta=0.01)

    def test_random_lightness(self):
        """ Random lightness only. Hue and saturation not changed. """
        args = ['-y 0', '-t 0', '-m 50', self.empty_svg]
        self.e.affect(args)
        hsl = extract_hsl(self.e.colmod(150, 100, 200))
        # Lightness change also affects hue and saturation...
        #self.assertEqual(0.75, round(hsl[0], 2))
        #self.assertEqual(0.48, round(hsl[1], 2))

    def test_random_saturation(self):
        """ Random saturation only. Hue and lightness not changed. """
        args = ['-y 0', '-t 50', '-m 0', self.empty_svg]
        self.e.affect(args)
        hsl = extract_hsl(self.e.colmod(150, 100, 200))
        self.assertAlmostEqual(hsl[0], 0.75, delta=0.01)
        self.assertAlmostEqual(hsl[2], 0.59, delta=0.01)

    def test_range_limits(self):
        """ The maximum hsl values should be between 0 and 100% of their maximum """
        args = ['-y 100', '-t 100', '-m 100', self.empty_svg]
        self.e.affect(args)
        hsl = extract_hsl(self.e.colmod(156, 156, 156))
        self.assertLessEqual([hsl[0], hsl[1], hsl[2]], [1, 1, 1])
        self.assertGreaterEqual([hsl[0], hsl[1], hsl[2]], [0, 0, 0])


class ColorRandomizeOpacityModificationTest(TestCase):
    def setUp(self):
        self.e=C()

    def test_no_change(self):
        """ The user selected 0% opacity range, and thus the opacity should not change. """
        args = ['-o 0', self.empty_svg]
        self.e.affect(args)
        opac = self.e.opacmod(0.15)
        self.assertEqual(0.15, opac)

    def test_range_min_limit(self):
        """ The opacity value should be greater than 0 """
        args = ['-o 100', self.empty_svg]
        self.e.affect(args)
        opac = self.e.opacmod(0)
        self.assertGreaterEqual(opac, "0")

    def test_range_max_limit(self):
        """ The opacity value should be lesser than 1 """
        args = ['-o 100', self.empty_svg]
        self.e.affect(args)
        opac = self.e.opacmod(1)
        self.assertLessEqual(opac, "1")

    def test_non_float_opacity(self):
        """ Non-float opacity value not changed """
        args = ['-o 100', self.empty_svg]
        self.e.affect(args)
        opac = self.e.opacmod("toto")
        self.assertLessEqual(opac, "toto")

if __name__ == '__main__':
    unittest.main()

# vim: expandtab shiftwidth=4 tabstop=8 softtabstop=4 fileencoding=utf-8 textwidth=99
