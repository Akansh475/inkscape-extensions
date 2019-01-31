#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unit test file for ../inkex.py
"""
# Revision history:
#   * 2012-01-27 (jazzynico): check errormsg function.
#

import unittest
from argparse import ArgumentTypeError
from tests.base import TestCase
from tests.base import StdRedirect
from inkex.utils import errormsg, addNS, inkbool, debug, to, filename_arg

class InkexBasicTest(TestCase):
    """Test basic utiltiies of inkex"""
    def test_inkbool(self):
        """Inkscape boolean input"""
        self.assertEqual(inkbool('TRUE'), True)
        self.assertEqual(inkbool('true'), True)
        self.assertEqual(inkbool('True'), True)
        self.assertEqual(inkbool('FALSE'), False)
        self.assertEqual(inkbool('false'), False)
        self.assertEqual(inkbool('False'), False)
        self.assertEqual(inkbool('Banana'), None)

    def test_debug(self):
        """Debug messages go to stderr"""
        with StdRedirect('stderr') as err:
            debug("Hello World")
            self.assertEqual(str(err), 'Hello World\n')

    def test_to(self):
        """Decorator for generators"""
        @to(list)
        def mylist(a, b, c):
            """Yield as a list"""
            yield a
            yield c
            yield b
        self.assertEqual(type(mylist(1, 2, 3)), list)
        self.assertEqual(mylist(1, 2, 3), [1, 3, 2])
        @to(dict)
        def mydict(a, b, c):
            """Yield as a dictionary"""
            yield ('age', a)
            yield ('name', c)
            yield ('home', b)
        self.assertEqual(type(mydict(1, 2, 3)), dict)
        self.assertEqual(mydict(1, 2, 3), {'age': 1, 'name': 3, 'home': 2})

    def test_filename(self):
        """Filename argument input"""
        self.assertEqual(filename_arg(__file__), __file__)
        self.assertRaises(ArgumentTypeError, filename_arg, 'doesntexist.txt')

    def test_add_ns(self):
        """Test addNS function"""
        self.assertEqual(
            addNS('inkscape:foo'),
            '{http://www.inkscape.org/namespaces/inkscape}foo')
        self.assertEqual(
            addNS('bar', 'inkscape'),
            '{http://www.inkscape.org/namespaces/inkscape}bar')
        self.assertEqual(
            addNS('url', 'rdf'),
            '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}url')
        self.assertEqual(
            addNS('{http://www.inkscape.org/namespaces/inkscape}bar'),
            '{http://www.inkscape.org/namespaces/inkscape}bar')
        self.assertEqual(
            addNS('http://www.inkscape.org/namespaces/inkscape:bar'),
            '{http://www.inkscape.org/namespaces/inkscape}bar')
        self.assertEqual(
            addNS('car', 'http://www.inkscape.org/namespaces/inkscape'),
            '{http://www.inkscape.org/namespaces/inkscape}car')
        self.assertEqual(
            addNS('{http://www.inkscape.org/namespaces/inkscape}bar', 'rdf'),
            '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}bar')

    def test_ascii(self):
        """Parse ABCabc"""
        with StdRedirect('stderr') as err:
            errormsg('ABCabc')
            self.assertEqual(str(err), 'ABCabc\n')

    def test_nonunicode_latin1(self):
        """Parse Àûïàèé"""
        with StdRedirect('stderr') as err:
            errormsg('Àûïàèé')
            self.assertEqual(str(err), 'Àûïàèé\n')

    def test_unicode_latin1(self):
        """Parse Àûïàèé (unicode)"""
        with StdRedirect('stderr') as err:
            errormsg(u'Àûïàèé')
            self.assertEqual(str(err), 'Àûïàèé\n')

if __name__ == '__main__':
    unittest.main()
