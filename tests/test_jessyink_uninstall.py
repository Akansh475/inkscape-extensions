# coding=utf-8
from jessyInk_uninstall import Uninstall
from inkex.tester import ComparisonMixin, TestCase

class JessyInkUninstallBasicTest(ComparisonMixin, TestCase):
    effect_class = Uninstall
