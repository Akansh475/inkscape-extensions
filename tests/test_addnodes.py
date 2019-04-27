# coding=utf-8
from addnodes import SplitIt
from inkex import NSS
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from inkex.tester.filters import CompareNumericFuzzy, CompareWithPathSpace

class SplitItBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = SplitIt
    compare_filters = [
        CompareWithPathSpace(),
        CompareNumericFuzzy(),
    ]

    def test_basic(self):
        args = ['--id=dashme',
                self.data_file('svg', 'dash.svg')]
        self.effect.run(args)
        old_path = self.effect.original_document.xpath('//svg:path', namespaces=NSS)[0].path
        new_path = self.effect.document.xpath('//svg:path', namespaces=NSS)[0].path
        assert len(new_path) > len(old_path)
