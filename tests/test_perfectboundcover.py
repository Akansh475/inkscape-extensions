# coding=utf-8
from perfectboundcover import PerfectBoundCover
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class PerfectBoundCoverBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = PerfectBoundCover
