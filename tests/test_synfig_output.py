# coding=utf-8
from synfig_output import SynfigExport
from tests.base import InkscapeExtensionTestMixin, TestCase


class TestSynfigExportBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = SynfigExport
        self.e = self.effect()
