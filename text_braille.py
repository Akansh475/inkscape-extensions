#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
if sys.version_info[0] < 3:
    chr = unichr

import chardataeffect

# https://en.wikipedia.org/wiki/Braille_ASCII#Braille_ASCII_values
U2801_MAP = "A1B'K2L@CIF/MSP\"E3H9O6R^DJG>NTQ,*5<-U8V.%[$+X!&;:4\\0Z7(_?W]#Y)="

def to_braille(c):
    assert isinstance(c, str)
    try:
        i = U2801_MAP.index(c.upper())
    except ValueError:
        return c
    return chr(i + 0x2801)

class C(chardataeffect.CharDataEffect):

  def process_chardata(self,text, line, par):
    return ''.join(map(to_braille, text))

if __name__ == '__main__':
    c = C()
    c.affect()
