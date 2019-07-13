# coding=utf-8
import pytest

from prepare_file_save_as import PrepareFileSave
from inkex.tester import ComparisonMixin, TestCase

class TestPrepareFileSaveBasic(ComparisonMixin, TestCase):
    effect_class = PrepareFileSave
    comparisons = [()]
