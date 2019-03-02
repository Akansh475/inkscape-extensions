#!/usr/bin/en

from tests.base import TestCase
import unittest
from convert2dashes import *

class DashitBasicTest(TestCase):
    effect = Dashit

    def test_basic(self):
        args = [
            '--id=dashme'
            , self.data_file('svg', 'dash.svg')]
        e = Dashit()
        e.run(args)
        old_dashes = e.original_document.xpath('//svg:path', namespaces=inkex.NSS)[0].path
        new_dashes = e.document.xpath('//svg:path', namespaces=inkex.NSS)[0].path
        self.assertTrue (len(new_dashes) > len (old_dashes))

if __name__ == '__main__':
    unittest.main()
