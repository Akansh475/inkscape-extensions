# coding=utf-8

import re

from jessyInk_video import JessyInk_Effects
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from inkex.tester.filters import Compare, CompareOrderIndependentBytes

class FilterOutJessyInkId(Compare):
    """Filter out jessyink ids specifically"""
    @staticmethod
    def filter(contents):
        return re.sub(br'jessyink.core.video\d+', b'jessyink.core.videoX', contents)

class JessyInkEffectsBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = JessyInk_Effects
    compare_filters = [FilterOutJessyInkId(), CompareOrderIndependentBytes()]
