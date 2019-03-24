#!/usr/bin/env python
# coding=utf-8

from chardataeffect import CharEffectBase

class TitleCase(CharEffectBase):
    def process_chardata(self, text):
        return text.title()

if __name__ == '__main__':
    TitleCase().run()
