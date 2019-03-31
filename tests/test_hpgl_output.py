# coding=utf-8
from hpgl_output import HpglOutput
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase


class HPGLOutputBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = HpglOutput
