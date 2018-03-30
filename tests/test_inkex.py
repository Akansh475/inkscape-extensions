#!/usr/bin/env python
#
# Unit test file for ../inkex.py
# Revision history:
#   * 2012-01-27 (jazzynico): check errormsg function.
#

from tests.base import TestCase, test_support
from inkex import errormsg

class InkexBasicTest(TestCase):
    def test_ascii(self):
        #Parse ABCabc
        errormsg('ABCabc')

    def test_nonunicode_latin1(self):
        #Parse Àûïàèé
        errormsg('Àûïàèé')

    def test_unicode_latin1(self):
        #Parse Àûïàèé (unicode)
        errormsg(u'Àûïàèé')

if __name__ == '__main__':
    test_support.run_unittest(InkexBasicTest)
