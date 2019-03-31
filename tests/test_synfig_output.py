# coding=utf-8
from synfig_output import SynfigExport
from tests.base import InkscapeExtensionTestMixin, TestCase

class TestSynfigExportBasic(InkscapeExtensionTestMixin, TestCase):
    effect_class = SynfigExport
