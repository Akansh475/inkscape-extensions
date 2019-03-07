# coding=utf-8
from param_curves import ParamCurves
from tests.base import InkscapeExtensionTestMixin, TestCase


class TestParamCurvesBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = ParamCurves
        self.e = self.effect()
