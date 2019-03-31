# coding=utf-8
from export_gimp_palette import ExportGpl
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class TestExportGplBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = ExportGpl
