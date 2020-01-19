#!/usr/bin/env python
"""Reverse the colors"""

import inkex

class Negative(inkex.ColorExtension):
    """Make the colour oposite"""
    def modify_color(self, name, color):
        # Support any colour space
        for i in range(3):
            color[i] = 255 - color[i]
        return color

if __name__ == '__main__':
    Negative().run()
