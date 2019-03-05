# coding=utf-8
from rtree import RTreeTurtle
from tests.base import InkscapeExtensionTestMixin, TestCase


class RTreeTurtleBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = RTreeTurtle
        self.e = self.effect()
