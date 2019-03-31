# coding=utf-8
from interp import Interp
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class InterpBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect = Interp
