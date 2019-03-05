# coding=utf-8
import sys

import pytest

from tests.base import InkscapeExtensionTestMixin, TestCase


@pytest.mark.skipif(sys.platform != 'win32', reason="Only runs on windows")
class TestPrintWin32VectorBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        from print_win32_vector import MyEffect
        self.effect = MyEffect
        self.e = self.effect()
