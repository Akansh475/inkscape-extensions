# coding=utf-8
from jessyInk_install import JessyInk_Install
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class JessyInkInstallBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = JessyInk_Install
