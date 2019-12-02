#!/usr/bin/env python
# coding=utf-8
"""Extension to remove the blue colour from selected shapes"""
from __future__ import absolute_import, division

import coloreffect

class RemoveBlue(coloreffect.ColorEffect):
    """Remove blue from the selected colors"""
    def colmod(self, r, g, b):
        return '{:02x}{:02x}{:02x}'.format(r, g, 0)

if __name__ == '__main__':
    RemoveBlue().run()
