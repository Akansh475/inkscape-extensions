#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import, division

import coloreffect


class C(coloreffect.ColorEffect):
    def colmod(self, r, g, b):
        factor = 0.9
        r = int(round(max(r * factor, 0)))
        g = int(round(max(g * factor, 0)))
        b = int(round(max(b * factor, 0)))
        return '{:02x}{:02x}{:02x}'.format(r, g, b)


if __name__ == '__main__':
    C().run()
