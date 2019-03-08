#!/usr/bin/env python
# coding=utf-8

import chardataeffect


class C(chardataeffect.CharDataEffect):

    def process_chardata(self, text, line, par):
        r = ""
        for i in range(len(text)):
            c = text[i]
            if c.islower():
                r = r + c.upper()
            elif c.isupper():
                r = r + c.lower()
            else:
                r = r + c

        return r


if __name__ == '__main__':
    C().run()
