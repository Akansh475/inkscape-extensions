#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import, division

import coloreffect


class C(coloreffect.ColorEffect):
    def colmod(self, r, g, b):
        # ITU-R Recommendation BT.709
        # l = 0.2125 * r + 0.7154 * g + 0.0721 * b

        # NTSC and PAL
        l = 0.299 * r + 0.587 * g + 0.114 * b

        ig = int(round(l))
        return '{:02x}{:02x}{:02x}'.format(ig, ig, ig)


if __name__ == '__main__':
    c = C()
    c.run()
