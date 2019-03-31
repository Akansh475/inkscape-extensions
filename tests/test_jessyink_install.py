# coding=utf-8
from jessyInk_install import JessyInk_Install
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class JessyInkInstallBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect = JessyInk_Install
