# coding=utf-8
from polyhedron_3d import Poly3D
from tests.base import InkscapeExtensionTestMixin, TestCase


class Poly3DBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Poly3D
        self.e = self.effect()
