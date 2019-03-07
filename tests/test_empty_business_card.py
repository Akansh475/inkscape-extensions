# coding=utf-8
from empty_business_card import BusinessCard
from tests.base import InkscapeExtensionTestMixin, TestCase


class TestBusinessCardBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = BusinessCard
        self.e = self.effect()
