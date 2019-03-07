# coding=utf-8
import os

from output_scour import ScourInkscape
from tests.base import InkscapeExtensionTestMixin, TestCase

# The current files directory
dir_path = os.path.dirname(os.path.realpath(__file__))


class ScourBasicTests(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = ScourInkscape
        self.e = self.effect()

    def test_working(self):
        input = os.path.join(dir_path, "data/svg/default-inkscape-SVG.svg")
        output = self.temp_file(suffix='.svg')
        output_expected = os.path.join(dir_path, "data/svg/default-inkscape-SVG_scoured.svg")

        self.e.run(['--output', output, input])

        with open(output_expected, 'rb') as f:
            self.assertEqual(self.e.document, f.read())
