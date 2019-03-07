# coding=utf-8
from synfig_prepare import SynfigPrep
from tests.base import InkscapeExtensionTestMixin, TestCase


class TestSynfigPrepBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = SynfigPrep
        self.e = self.effect()
