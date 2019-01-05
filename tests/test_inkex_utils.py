#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unit test file for ../inkex.py
"""
# Revision history:
#   * 2012-01-27 (jazzynico): check errormsg function.
#

import unittest
from tests.base import TestCase
from tests.base import StdRedirect
from inkex.utils import errormsg, addNS

class InkexBasicTest(TestCase):
    """Test basic utiltiies of inkex"""
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
