#!/usr/bin/en
# coding=utf-8
from jessyInk_effects import JessyinkEffects
from inkex.tester import ComparisonMixin, TestCase

class JessyInkEffectsTest(ComparisonMixin, TestCase):
    effect_class = JessyinkEffects
    comparisons = [
        ('--id=p1', '--id=r3')
    ]
