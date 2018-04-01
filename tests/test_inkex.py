#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unit test file for ../inkex.py
"""
# Revision history:
#   * 2012-01-27 (jazzynico): check errormsg function.
#

from tests.base import TestCase, PrintedOutput, test_support
from inkex.utils import errormsg

class InkexBasicTest(TestCase):
    """Test basic utiltiies of inkex"""
    def test_ascii(self):
        """Parse ABCabc"""
        with PrintedOutput('stderr') as err:
            errormsg('ABCabc')
            self.assertEqual(str(err), 'ABCabc\n')

    def test_nonunicode_latin1(self):
        """Parse Àûïàèé"""
        with PrintedOutput('stderr') as err:
            errormsg('Àûïàèé')
            self.assertEqual(str(err), 'Àûïàèé\n')

    def test_unicode_latin1(self):
        """Parse Àûïàèé (unicode)"""
        with PrintedOutput('stderr') as err:
            errormsg(u'Àûïàèé')
            self.assertEqual(str(err), 'Àûïàèé\n')

if __name__ == '__main__':
    test_support.run_unittest(InkexBasicTest)
