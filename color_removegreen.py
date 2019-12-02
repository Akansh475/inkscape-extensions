#!/usr/bin/env python
# coding=utf-8
"""Remove green color from selected objects"""
from __future__ import absolute_import, division

import coloreffect

class RemoveGreen(coloreffect.ColorEffect):
    """Remove green color from objects"""
    def colmod(self, r, g, b):
        return '{:02x}{:02x}{:02x}'.format(r, 0, b)

if __name__ == '__main__':
    RemoveGreen().run()
