#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import, division

import coloreffect

class Negative(coloreffect.ColorEffect):
    """Make the colour oposite"""
    def colmod(self, r, g, b):
        return "{:02x}{:02x}{:02x}".format(255 - r, 255 - g, 255 - b)

if __name__ == '__main__':
    Negative().run()
