# coding=utf-8
from setup_typography_canvas import SetupTypographyCanvas
from tests.base import InkscapeExtensionTestMixin, TestCase

class TestSetupTypographyCanvasBasic(InkscapeExtensionTestMixin, TestCase):
    effect_class = SetupTypographyCanvas
