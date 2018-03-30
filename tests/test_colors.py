#!/usr/bin/env python

from tests.base import TestCase, test_support
from inkex.styles import parseStyle
from inkex.colors import parseColor

class ParseColorTest(TestCase):
    """Test for single transformations"""
    def test_namedcolor(self):
        "Parse 'red'"
        col = parseColor('red')
        self.assertEqual((255,0,0), col)
        
    def test_hexcolor4digit(self):
        "Parse '#ff0102'"
        col = parseColor('#ff0102')
        self.assertEqual((255,1,2), col)
        
    def test_hexcolor3digit(self):
        "Parse '#fff'"
        col = parseColor('#fff')
        self.assertEqual((255,255,255), col)
        
    def test_rgbcolorint(self):
        "Parse 'rgb(255,255,255)'"
        col = parseColor('rgb(255,255,255)')
        self.assertEqual((255,255,255),col)
        
    def test_rgbcolorpercent(self):
        "Parse 'rgb(100%,100%,100%)'"
        col = parseColor('rgb(100%,100%,100%)')
        self.assertEqual((255,255,255),col)
        
    def test_rgbcolorpercent2(self):
        "Parse 'rgb(100%,100%,100%)'"
        col = parseColor('rgb(50%,0%,1%)')
        self.assertEqual((127,0,2),col)
        
    def test_rgbcolorpercentdecimal(self):
        "Parse 'rgb(66.667%,0%,6.667%)'"
        col = parseColor('rgb(66.667%,0%,6.667%)')
        self.assertEqual((170, 0, 17),col)
    
    # TODO: This test appears to be broken.  parseColor can
    #       only return an RGB colour code
    #def test_currentColor(self):
    #    "Parse 'currentColor'"
    #    col = parseColor('currentColor')
    #    self.assertEqual(('currentColor'),col)

    def test_spaceinstyle(self):
        "Parse 'stop-color: rgb(0,0,0)'"
        col = parseStyle('stop-color: rgb(0,0,0)')
        self.assertEqual({'stop-color': 'rgb(0,0,0)'},col)

    #def test_unknowncolor(self):
    #    "Parse 'unknown'"
    #    col = parseColor('unknown')
    #    self.assertEqual((0,0,0),col)
    #
    
if __name__ == '__main__':
    test_support.run_unittest(ParseColorTest)
