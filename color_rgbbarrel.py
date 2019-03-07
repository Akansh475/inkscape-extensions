#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import, division

import coloreffect


class C(coloreffect.ColorEffect):
    """
    Cycle colors RGB -> BRG

    aka  Do a Barrel Roll!

    """

    def colmod(self, r, g, b):
        return '{:02x}{:02x}{:02x}'.format(b, r, g)


if __name__ == '__main__':
    C().run()
