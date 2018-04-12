#!/usr/bin/env python
import chardataeffect

class C(chardataeffect.CharDataEffect):
  def process_chardata(self, text, line=False, par=False):
    return text.lower()

if __name__ == '__main__':
    c = C()
    c.affect()
