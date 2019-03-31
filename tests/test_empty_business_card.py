# coding=utf-8
from empty_business_card import BusinessCard
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase


class TestBusinessCardBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = BusinessCard
