#!/usr/bin/env python
# coding=utf-8

from chardataeffect import CharEffectBase

class Uppercase(CharEffectBase):
    def process_chardata(self, text):
        return text.upper()

if __name__ == '__main__':
    Uppercase().run()
