"""Test base inkex module functionality"""

import os
import sys

from inkex.base import InkscapeExtension, SvgThroughMixin
from tests.base import TestCase, StdRedirect

class ModExtension(InkscapeExtension):
    """A non-svg extension that loads, saves and flipples"""
    def effect(self):
        self.document += '>flipple'

    def load(self, stream):
        return stream.read()

    def save(self, stream):
        stream.write(self.document)

class NoModSvgExtension(SvgThroughMixin, InkscapeExtension):
    """Test the loading and not-saving of non-modified svg files"""
    def effect(self):
        return True

class ModSvgExtension(SvgThroughMixin, InkscapeExtension):
    """Test the loading and saving of svg files"""
    def effect(self):
        self.svg.set('attr', 'foo')


class InkscapeExtensionTest(TestCase):
    """Tests for Inkscape Extensions"""
    def setUp(self):
        self.obj = InkscapeExtension()

    def test_bare_bones(self):
        """What happens when we don't inherit"""
        with self.assertRaises(NotImplementedError):
            self.obj.run([])
        with self.assertRaises(NotImplementedError):
            self.obj.effect()
        with self.assertRaises(NotImplementedError):
            self.obj.load(sys.stdin)
        with self.assertRaises(NotImplementedError):
            self.obj.save(sys.stdout)
        self.assertEqual(self.obj.name, 'InkscapeExtension')

    def test_compat(self):
        """Test a few old functions and how we handle them"""
        with self.assertRaises(AttributeError):
            self.assertEqual(self.obj.OptionParser, None)
        with self.assertRaises(AttributeError):
            self.assertEqual(self.obj.affect(), None)

    def test_arg_parser_defaults(self):
        """Test arguments for the base class are given defaults"""
        options = self.obj.arg_parser.parse_args([])
        self.assertEqual(options.input_file.name, '<stdin>') # Python 3 compatible
        self.assertEqual(options.output.name, '<stdout>') # Python 3 compatible

    def test_arg_parser_passed(self):
        """Test arguments for the base class are parsed"""
        options = self.obj.arg_parser.parse_args(['--output', 'foo.txt', self.empty_svg])
        self.assertEqual(options.input_file, self.empty_svg)
        self.assertEqual(options.output, 'foo.txt')

    def test_output(self):
        """Test the ins and outs of an extension"""
        with StdRedirect() as output:
            with StdRedirect('stdin', 'dinner'):
                ModExtension().run([])
                self.assertEqual(str(output), 'dinner>flipple')


class SvgInputOutputTest(TestCase):
    """Test SVG Input Mixin"""
    def test_input_mixin(self):
        """Test svg input gets loaded"""
        obj = NoModSvgExtension()
        obj.run([self.empty_svg])
        self.assertNotEqual(obj.document, None)
        self.assertNotEqual(obj.original_document, None)

    def test_no_output(self):
        """Test svg output isn't saved when not modified"""
        obj = NoModSvgExtension()
        filename = self.temp_file(suffix='.svg')
        obj.run(['--output', filename, self.empty_svg])
        self.assertEqual(type(obj.document).__name__, '_ElementTree')
        self.assertEqual(type(obj.svg).__name__, 'SvgDocumentElement')
        self.assertFalse(os.path.isfile(filename))

    def test_svg_output(self):
        """Test svg output is saved"""
        obj = ModSvgExtension()
        filename = self.temp_file(suffix='.svg')
        obj.run(['--output', filename, self.empty_svg])
        self.assertTrue(os.path.isfile(filename))
        with open(filename, 'r') as fhl:
            self.assertIn('<svg', fhl.read())
