#!/usr/bin/env python
# coding=utf-8

import random

from chardataeffect import CharEffectBase

class RandomCase(CharEffectBase):
    """Randomise the case of the text (with bias)"""
    previous_case = 1

    def map_char(self, char):
        # bias the randomness towards inversion of the previous case:
        if self.previous_case > 0:
            case = random.choice([-2, -1, 1])
        else:
            case = random.choice([-1, 1, 2])

        if char.isalpha():
            self.previous_case = case
            if case > 0:
                return char.upper()
            elif case < 0:
                return char.lower()
        return char

if __name__ == '__main__':
    RandomCase().run()
