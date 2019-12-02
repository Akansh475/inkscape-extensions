#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import, division

import coloreffect

class Brighter(coloreffect.ColorEffect):
    """Make colours brighter"""
    def colmod(self, r, g, b):
        factor = 0.9

        i = int(1 / (1 - factor))

        if r == 0 and g == 0 and b == 0:
            return '{:02x}{:02x}{:02x}'.format(i, i, i)

        if 0 < r < i:
            r = i
        if 0 < g < i:
            g = i
        if 0 < b < i:
            b = i

        r = min(int(round((r / factor))), 255)
        g = min(int(round((g / factor))), 255)
        b = min(int(round((b / factor))), 255)

        return '{:02x}{:02x}{:02x}'.format(r, g, b)

if __name__ == '__main__':
    Brighter().run()
