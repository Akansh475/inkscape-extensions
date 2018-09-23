#!/usr/bin/env python
"""
Test Inkex path parsing functionality.
"""

from tests.base import TestCase, test_support

from inkex.paths import Path, PathCommand, InvalidPath

class PathTest(TestCase):
    """Test path API and calculations"""
    def test_new_empty(self):
        """Create a path from a path string"""
        self.assertEqual(str(Path()), '')

    def test_invalid(self):
        """Load an invalid path"""
        self.assertEqual(str(Path('& 10 10 M 20 20')), 'M 20 20')
        self.assertRaises(InvalidPath, PathCommand, '&')
        self.assertRaises(InvalidPath, PathCommand, 'Z', 40)

    def test_repr(self):
        """Path representation"""
        self.assertEqual(repr(Path('M 10 10 10 10')), "[Move('M', 10, 10), Line('L', 10, 10)]")

    def test_list(self):
        """Path of previous commands"""
        path = Path(Path('M 10 10 20 20 30 30 Z')[1:-1])
        self.assertEqual(str(path), 'L 20 20 L 30 30')

    def test_passthrough(self):
        """Create a path and test the re-rendering of the commands"""
        for path in (
                'M 50,50 L 10,10 m 10 10 l 2.1,2',
                'm 150 150 c 10 10 6 6 20 10 L 10 10',
            ):
            self.assertEqual(str(Path(path)), path.replace(',', ' '))

    def test_chained_conversion(self):
        """Paths always extrapolate chained commands"""
        for path, ret in (
                ('M 100 100 20 20', 'M 100 100 L 20 20'),
                ('M 100 100 Z 20 20', 'M 100 100 Z L 20 20'),
                ('M 100 100 L 20 20 40 40 30 10 Z', 'M 100 100 L 20 20 L 40 40 L 30 10 Z'),
                ('m 50 50 l 20 20 40 40', 'm 50 50 l 20 20 l 40 40'),
                ('m 50 50 20 20', 'm 50 50 l 20 20'),
            ):
            self.assertEqual(str(Path(path)), ret)

    def test_points(self):
        """Test how x,y points are extracted"""
        for path, ret in (
                ('M 100 100', ((100, 100),)),
                ('L 100 100', ((100, 100),)),
                ('H 133', ((133, None),)),
                ('V 144', ((None, 144),)),
                ('T 100 100', ((100, 100),)),
                ('C 12 12 15 15 20 20', ((12, 12), (15, 15), (20, 20))),
                ('S 50 90 30 10', ((50, 90), (30, 10),)),
                ('Q 40 20 12 99', ((40, 20), (12, 99),)),
                ('A 1,2,3,4,5,10,20', ((10, 20),)),
                ('Z', ()),
            ):
            self.assertEqual(Path(path)[0].points, ret)

    def test_adding_to_path(self):
        """Paths can be translated using addition"""
        ret = Path('M 20,20 L 90,90 l 10,10 Z') + (50, 50)
        self.assertEqual(str(ret), 'M 70 70 L 140 140 l 10 10 Z')

    def test_extending(self):
        """Paths can be extended using addition"""
        ret = Path('M 20 20') + Path('L 40 40 9 10')
        self.assertEqual(type(ret), Path)
        self.assertEqual(str(ret), 'M 20 20 L 40 40 L 9 10')

        ret = Path('M 20 20') + 'C 40 40 9 10 10 10'
        self.assertEqual(type(ret), Path)
        self.assertEqual(str(ret), 'M 20 20 C 40 40 9 10 10 10')

    def test_subtracting_from_path(self):
        """Paths can be translated using addition"""
        ret = Path('M 20,20 L 90,90 l 10,10 Z') - (10, 10)
        self.assertEqual(str(ret), 'M 10 10 L 80 80 l 10 10 Z')

    def test_scale(self):
        """Paths can be scaled using the times operator"""
        ret = Path('M 10,10 L 30,30 C 20 20 10 10 10 10 l 10 10') * (2.5, 3)
        self.assertEqual(str(ret), 'M 25 30 L 75 90 C 50 60 25 30 25 30 l 25 30')

        ret = Path("M 29.867708,101.68274 A 14.867708,14.867708 0 0 1 15,116.55045 14.867708,"\
            "14.867708 0 0 1 0.13229179,101.68274 14.867708,14.867708 0 0 1 15,86.815031 "\
            "14.867708,14.867708 0 0 1 29.867708,101.68274 Z")
        ret.scale(1.2, 0.8)
        self.assertEqual(str(ret), 'M 35.8412 81.3462 A 17.8412 17.8412 0 0 1 '\
            '18 93.2404 A 17.8412 17.8412 0 0 1 0.15875 81.3462 A 17.8412 1'\
            '7.8412 0 0 1 18 69.452 A 17.8412 17.8412 0 0 1 35.8412 81.3462 Z')


    def test_absolute(self):
        """Paths can be converted to absolute"""
        ret = Path("M 100 100 l 10 10 10 10 10 10")
        ret.to_absolute()
        self.assertEqual(str(ret), "M 100 100 L 110 110 L 120 120 L 130 130")

        ret = Path("M 100 100 h 10 10 10 v 10 10 10")
        ret.to_absolute()
        self.assertEqual(str(ret), "M 100 100 H 110 H 120 H 130 V 110 V 120 V 130")

        ret = Path("M 150,150 a 76,55 0 1 1 283,128")
        ret.to_absolute()
        self.assertEqual(str(ret), "M 150 150 A 76 55 0 1 1 433 278")

    def test_relative(self):
        """Paths can be converted to relative"""
        ret = Path("M 100 100 L 110 120 140 140 300 300")
        ret.to_relative()
        self.assertEqual(str(ret), "m 100 100 l 10 20 l 30 20 l 160 160")

        ret = Path("M 150,150 A 76,55 0 1 1 433,278")
        ret.to_relative()
        self.assertEqual(str(ret), "m 150 150 a 76 55 0 1 1 283 128")

    def test_rotate(self):
        """Paths can be rotated"""
        ret = Path("M 29.867708,101.68274 A 14.867708,14.867708 0 0 1 15,116.55045 14.867708,"\
            "14.867708 0 0 1 0.13229179,101.68274 14.867708,14.867708 0 0 1 15,86.815031 "\
            "14.867708,14.867708 0 0 1 29.867708,101.68274 Z")
        ret.rotate(33, 113.394 / 2, 113.394 / 2)
        self.assertEqual(str(ret), "M 27.469109,109.78027 A 14.867708,14.86770'\
            '8 0 0 1 6.9024649,114.15185 14.867708,14.867708 0 0 1 2.5308909,9'\
            '3.585206 14.867708,14.867708 0 0 1 23.097535,89.21363 a 14.867708'\
            ',14.867708 0 0 1 4.371574,20.56664 z")
        ret.rotate(-33, 113.394 / 2, 113.394 / 2)
        self.assertEqual(str(ret), "M 29.867708,101.68274 A 14.867708,14.86770'\
            '8 0 0 1 15,116.55045 14.867708,14.867708 0 0 1 0.13229179,101.682'\
            '74 14.867708,14.867708 0 0 1 15,86.815031 14.867708,14.867708 0 0'\
            ' 1 29.867708,101.68274 Z")
        ret.rotate(40, 113.394 / 2, 113.394 / 2)
        self.assertEqual(str(ret), "M 26.389325,111.23952 A 14.867708,14.86770'\
            '8 0 0 1 5.4432204,113.07207 14.867708,14.867708 0 0 1 3.6106749,9'\
            '2.125962 14.867708,14.867708 0 0 1 24.556779,90.293414 14.867708,'\
            '14.867708 0 0 1 26.389325,111.23952 Z")
        ret.rotate(40, 113.394 / 2, 113.394 / 2)
        self.assertEqual(str(ret), "M 17.58175,116.32458 A 14.867708,14.867708'\
            ' 0 0 1 0.35816272,104.26449 14.867708,14.867708 0 0 1 12.41825,87'\
            '.040907 14.867708,14.867708 0 0 1 29.641836,99.10099 14.867708,14'\
            '.867708 0 0 1 17.58175,116.32458 Z")


if __name__ == '__main__':
    test_support.run_unittest(PathTest)
