#!/usr/bin/env python
# coding=utf-8
import chardataeffect


class C(chardataeffect.CharDataEffect):
    def process_chardata(self, text, line=False, par=False):
        return text.lower()


if __name__ == '__main__':
    C().run()
