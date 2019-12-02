#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import, division

import coloreffect

class Grayscale(coloreffect.ColorEffect):
    """Make all colours grayscale"""
    def colmod(self, r, g, b):
        # ITU-R Recommendation BT.709
        # l = 0.2125 * r + 0.7154 * g + 0.0721 * b

        # NTSC and PAL
        lum = 0.299 * r + 0.587 * g + 0.114 * b
        gray = int(round(lum))
        return '{:02x}{:02x}{:02x}'.format(gray, gray, gray)

if __name__ == '__main__':
    Grayscale().run()
