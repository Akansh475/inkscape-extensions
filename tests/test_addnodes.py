# coding=utf-8
from addnodes import AddNodes
from inkex.tester import ComparisonMixin, TestCase
from inkex.tester.filters import CompareNumericFuzzy, CompareWithPathSpace

class SplitItBasicTest(ComparisonMixin, TestCase):
    effect_class = AddNodes
    comparisons = [("--id=p1", "--id=r3", "--max=2.0",)]
    compare_filters = [
        CompareWithPathSpace(),
        CompareNumericFuzzy(),
    ]

    def test_basic(self):
        args = ['--id=dashme',
                self.data_file('svg', 'dash.svg')]
        effect = self.effect_class()
        effect.run(args)
        old_path = effect.original_document.getroot().getElement('//svg:path').path
        new_path = effect.svg.getElement('//svg:path').path
        assert len(new_path) > len(old_path)
