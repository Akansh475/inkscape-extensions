#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import, division

import coloreffect


class C(coloreffect.ColorEffect):
    def colmod(self, r, g, b):
        return '{:02x}{:02x}{:02x}'.format(0, g, b)


if __name__ == '__main__':
    c = C()
    c.run()
