#!/usr/bin/env python
# coding=utf-8

import chardataeffect


def _process_letter(c):
    return c.upper() if c.islower() else c.lower()


class C(chardataeffect.CharDataEffect):

    def process_chardata(self, text, line, par):
        return ''.join(map(_process_letter, text))


if __name__ == '__main__':
    C().run()
