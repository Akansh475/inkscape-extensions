# coding=utf-8
from param_curves import ParamCurves
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.filters import CompareNumericFuzzy, CompareWithPathSpace

class TestParamCurvesBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect = ParamCurves
    compare_filters = [CompareNumericFuzzy(), CompareWithPathSpace()]
