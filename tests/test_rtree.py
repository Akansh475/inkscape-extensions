# coding=utf-8
from rtree import RTreeTurtle
from inkex.tester import InkscapeExtensionTestMixin, TestCase

class RTreeTurtleBasicTest(InkscapeExtensionTestMixin, TestCase):
    effect_class = RTreeTurtle
