#!/usr/bin/env python
# coding=utf-8

from perspective import PathPerspective
from inkex.tester import ComparisonMixin, TestCase

class PerspectiveBasicTest(ComparisonMixin, TestCase):
    effect_class = PathPerspective
    comparisons = [('--id=p1', '--id=p2')]
