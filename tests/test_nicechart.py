# coding=utf-8
from nicechart import NiceChart
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from inkex.tester.filters import CompareNumericFuzzy

class TestNiceChartBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = NiceChart
    compare_file = 'svg/default-plain-SVG.svg'
    compare_filters = [CompareNumericFuzzy()]

    @property
    def comparisons(self):
        filename = self.data_file('nicechart_01.csv')
        filearg = '--file={}'.format(filename)
        return (
            (filearg,),
            (filearg, '--type=pie'),
            (filearg, '--type=pie_abs'),
            (filearg, '--type=stbar'),
        )
