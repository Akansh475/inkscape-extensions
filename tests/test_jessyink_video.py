# coding=utf-8

import re

from jessyInk_video import Video
from inkex.tester import ComparisonMixin, TestCase
from inkex.tester.filters import Compare, CompareOrderIndependentBytes

class FilterOutJessyInkId(Compare):
    """Filter out jessyink ids specifically"""
    @staticmethod
    def filter(contents):
        return re.sub(br'jessyink.core.video\d+', b'jessyink.core.videoX', contents)

class JessyInkEffectsBasicTest(ComparisonMixin, TestCase):
    effect_class = Video
    compare_filters = [FilterOutJessyInkId(), CompareOrderIndependentBytes()]
