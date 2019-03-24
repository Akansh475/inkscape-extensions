#!/usr/bin/env python
# coding=utf-8

from chardataeffect import CharEffectBase


class FlipCase(CharEffectBase):
    """Change the case, cHANGE THE CASE"""
    @staticmethod
    def map_char(char):
        return char.upper() if char.islower() else char.lower()

if __name__ == '__main__':
    FlipCase().run()
