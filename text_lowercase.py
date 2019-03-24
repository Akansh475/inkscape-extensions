#!/usr/bin/env python
# coding=utf-8

from chardataeffect import CharEffectBase

class Lowercase(CharEffectBase):
    def process_chardata(self, text):
        return text.lower()

if __name__ == '__main__':
    Lowercase().run()
