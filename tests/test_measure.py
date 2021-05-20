# coding=utf-8
from inkex.utils import filename_arg
from measure import MeasureLength
from inkex.tester import ComparisonMixin, TestCase
from inkex.tester.filters import CompareNumericFuzzy

class LengthBasicTest(ComparisonMixin, TestCase):
    effect_class = MeasureLength
    compare_filters = [CompareNumericFuzzy()]
    comparisons = [
        ('--id=p1', '--id=p2'),
        ('--method=presets', '--presetFormat=TaP_start', '--id=p1'),
        ('--method=presets', '--presetFormat=TaP_end', '--id=p2'),
        ('--method=presets', '--presetFormat=FT_start', '--id=p1'),
        ('--method=presets', '--presetFormat=FT_bbox', '--id=p2'),
        ('--method=presets', '--presetFormat=FT_bbox', '--id=p2'),
        ('--type=area', '--id=p1'),
        ('--type=cofm', '--id=c3'),
    ]

class LengthComplexTransformTest(ComparisonMixin, TestCase):
    effect_class = MeasureLength
    compare_filters = [CompareNumericFuzzy()]
    compare_file = "svg/complextransform.test.svg"
    comparisons = [
        ('--method=presets', '--presetFormat=TaP_start', '--id=D'),
        ('--method=presets', '--presetFormat=FT_start', '--id=D'),
        ('--type=cofm', '--id=D'),
    ]
