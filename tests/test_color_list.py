# coding=utf-8
from color_list import ColorList
from .test_inkex_extensions import ColorEffectTest

class ColorListTest(ColorEffectTest):
    effect_class = ColorList
    effect_name = 'test_color_list'
    stderr_output = True
    color_tests = []
