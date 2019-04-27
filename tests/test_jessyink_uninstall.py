# coding=utf-8
from jessyInk_uninstall import JessyInk_Uninstall
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class JessyInkUninstallBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = JessyInk_Uninstall
