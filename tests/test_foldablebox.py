#!/usr/bin/env python

from unittest import TestCase
import unittest
from foldablebox import *

class FoldableBoxArguments(TestCase):
    effect = FoldableBox

    def test_basic_box_elements(self):
        e = FoldableBox()
        e.affect([self.empty_svg])
        self.assertEqual( e.box.tag, 'g', 'The box group must be created.' )
        self.assertEqual( len( e.box.getchildren() ), 13, 'The box group must have 13 childs.' )

if __name__ == '__main__':
    unittest.main()
