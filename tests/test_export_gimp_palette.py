# coding=utf-8
from export_gimp_palette import ExportGpl
from tests.base import InkscapeExtensionTestMixin, TestCase


class TestExportGplBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = ExportGpl
        self.e = self.effect()
