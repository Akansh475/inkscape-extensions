# coding=utf-8

from path_envelope import PathEnvelope
from inkex.tester import ComparisonMixin, TestCase

class PathEnvelopeTest(ComparisonMixin, TestCase):
    """Test envelope similar to perspective"""
    effect_class = PathEnvelope
    comparisons = [('--id=text', '--id=envelope')]
    compare_file = 'svg/perspective.svg'
