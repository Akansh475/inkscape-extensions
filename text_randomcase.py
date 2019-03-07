#!/usr/bin/env python

import random
import chardataeffect

class C(chardataeffect.CharDataEffect):
  def process_chardata(self,text, line, par):
    r = ""
    a = 1
    for i in range(len(text)):
      c = text[i]
      # bias the randomness towards inversion of the previous case:
      if a > 0:
        a = random.choice([-2,-1,1])
      else:
        a = random.choice([-1,1,2])
      if a > 0 and c.isalpha():
        r = r + c.upper()
      elif a < 0 and c.isalpha():
        r = r + c.lower()
      else:
        r = r + c

    return r

if __name__ == '__main__':
    C().run()
