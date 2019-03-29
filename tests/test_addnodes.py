# coding=utf-8
from addnodes import SplitIt
from inkex import NSS
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.filters import CompareNumericFuzzy, CompareWithPathSpace

class SplitItBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect = SplitIt
    compare_filters = [
        CompareWithPathSpace(),
        CompareNumericFuzzy(),
    ]

    def setUp(self):
        self.e = self.effect()

    def test_basic(self):
        args = ['--id=dashme',
                self.data_file('svg', 'dash.svg')]
        self.e.run(args)
        old_path = self.e.original_document.xpath('//svg:path', namespaces=NSS)[0].path
        new_path = self.e.document.xpath('//svg:path', namespaces=NSS)[0].path
        assert len(new_path) > len(old_path)
