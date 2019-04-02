#!/usr/bin/env python
from webslicer_create_group import WebSlicer_CreateGroup
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class TestWebSlicerCreateGroupBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = WebSlicer_CreateGroup
    comparisons = [('--id', 'slicerect1')]
