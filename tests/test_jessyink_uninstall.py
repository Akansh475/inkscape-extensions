# coding=utf-8
from jessyInk_uninstall import JessyInk_Uninstall
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class JessyInkUninstallBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = JessyInk_Uninstall
