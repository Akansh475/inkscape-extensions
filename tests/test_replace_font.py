# coding=utf-8
from replace_font import ReplaceFont
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.filters import CompareOrderIndependentStyle

class TestReplaceFontBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = ReplaceFont
    compare_filters = [CompareOrderIndependentStyle()]
    comparisons =[(
        '--action=find_replace',
        '--fr_find=sans-serif',
        '--fr_replace=monospace',
    )]
