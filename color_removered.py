#!/usr/bin/env python
# coding=utf-8
"""Extension for removing the colour red from selected objects"""
from __future__ import absolute_import, division

import coloreffect

class RemoveRed(coloreffect.ColorEffect):
    """Remove red color from selected objects"""
    def colmod(self, r, g, b):
        return '{:02x}{:02x}{:02x}'.format(0, g, b)

if __name__ == '__main__':
    RemoveRed().run()
