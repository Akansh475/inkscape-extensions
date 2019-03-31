# coding=utf-8
from convert2dashes import Dashit
from inkex import NSS
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase


class DashitBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    comparisons = ([],)
    effect_class = Dashit

    def test_basic(self):
        args = ['--id=dashme',
                self.data_file('svg', 'dash.svg')]
        self.effect.run(args)
        old_dashes = self.effect.original_document.xpath('//svg:path', namespaces=NSS)[0].path
        new_dashes = self.effect.document.xpath('//svg:path', namespaces=NSS)[0].path
        assert len(new_dashes) > len(old_dashes)
