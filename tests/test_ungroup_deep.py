# coding=utf-8
from tests.base import InkscapeExtensionTestMixin, TestCase
from ungroup_deep import Ungroup

class TestUngroupBasic(InkscapeExtensionTestMixin, TestCase):
    effect_class = Ungroup
