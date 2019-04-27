# coding=utf-8
import sys

import pytest

from print_win32_vector import MyEffect
from inkex.tester import InkscapeExtensionTestMixin, TestCase

@pytest.mark.skipif(sys.platform != 'win32', reason="Only runs on windows")
class TestPrintWin32VectorBasic(InkscapeExtensionTestMixin, TestCase):
    effect_class = MyEffect
