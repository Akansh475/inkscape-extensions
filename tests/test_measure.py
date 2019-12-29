# coding=utf-8
from measure import MeasureLength
from inkex.tester import ComparisonMixin, TestCase

class LengthBasicTest(ComparisonMixin, TestCase):
    effect_class = MeasureLength
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
