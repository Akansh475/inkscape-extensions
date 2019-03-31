# coding=utf-8
from jessyInk_masterSlide import JessyInk_MasterSlide
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class JessyInkMasterSlideBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = JessyInk_MasterSlide
