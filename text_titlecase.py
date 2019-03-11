#!/usr/bin/env python
# coding=utf-8
import chardataeffect


class TitleCase(chardataeffect.CharDataEffect):

    def process_chardata(self, text, line, par):
        return text.title()

if __name__ == '__main__':
    TitleCase().run()
