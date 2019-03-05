# coding=utf-8
from empty_generic import GenericTemplate
from tests.base import InkscapeExtensionTestMixin, TestCase


class TestGenericTemplateBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = GenericTemplate
        self.e = self.effect()
