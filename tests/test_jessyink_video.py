# coding=utf-8

import re

from jessyInk_video import JessyInk_Effects
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.filters import Compare

class FilterOutJessyInkId(Compare):
    """Filter out jessyink ids specifically"""
    @staticmethod
    def filter(contents):
        return re.sub(br'jessyink.core.video\d+', b'jessyink.core.videoX', contents)

class JessyInkEffectsBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect = JessyInk_Effects
    compare_filters = [FilterOutJessyInkId()]
