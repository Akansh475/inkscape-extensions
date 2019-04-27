# coding=utf-8

import re

from ps_input import PostscriptInput

from tests.base.filters import CompareSize
from tests.base import ComparisonMixin, TestCase

class TestPostscriptInput(ComparisonMixin, TestCase):
    effect_class = PostscriptInput
    compare_filters = [CompareSize()]
    compare_file = [
        'ref_test.ps',
        'ref_test.eps',
    ]
    comparisons = [()]
