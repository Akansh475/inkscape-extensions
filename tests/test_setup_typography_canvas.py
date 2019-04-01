# coding=utf-8
from setup_typography_canvas import SetupTypographyCanvas
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class TestSetupTypographyCanvasBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = SetupTypographyCanvas
