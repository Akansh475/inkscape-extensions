# coding=utf-8
"""
Test Inkex path parsing functionality.
"""

import re

from inkex.paths import InvalidPath, Path, PathCommand
from inkex.transforms import BoundingBox, Transform
from tests.base import TestCase


class PathTest(TestCase):
    """Test path API and calculations"""

    def _assertPath(self, path, want_string):
        """Test a normalized path string against a good value"""
        return self.assertEqual(re.sub('\\s+', ' ', str(path)), want_string)

    def test_new_empty(self):
        """Create a path from a path string"""
        self.assertEqual(str(Path()), '')

    def test_invalid(self):
        """Load an invalid path"""
        self._assertPath(Path('& 10 10 M 20 20'), 'M 20 20')
        self.assertRaises(InvalidPath, PathCommand, '&')
        self.assertRaises(InvalidPath, PathCommand, 'Z', 40)

    def test_copy(self):
        """Make a copy of a path"""
        self.assertEqual(str(Path('M 10 10').copy()), 'M 10 10')

    def test_repr(self):
        """Path representation"""
        self._assertPath(repr(Path('M 10 10 10 10')), "[Move('M', 10, 10), Line('L', 10, 10)]")

    def test_list(self):
        """Path of previous commands"""
        path = Path(Path('M 10 10 20 20 30 30 Z')[1:-1])
        self._assertPath(path, 'L 20 20 L 30 30')

    def test_passthrough(self):
        """Create a path and test the re-rendering of the commands"""
        for path in (
                'M 50,50 L 10,10 m 10 10 l 2.1,2',
                'm 150 150 c 10 10 6 6 20 10 L 10 10',
        ):
            self._assertPath(Path(path), path.replace(',', ' '))

    def test_chained_conversion(self):
        """Paths always extrapolate chained commands"""
        for path, ret in (
                ('M 100 100 20 20', 'M 100 100 L 20 20'),
                ('M 100 100 Z 20 20', 'M 100 100 Z L 20 20'),
                ('M 100 100 L 20 20 40 40 30 10 Z', 'M 100 100 L 20 20 L 40 40 L 30 10 Z'),
                ('m 50 50 l 20 20 40 40', 'm 50 50 l 20 20 l 40 40'),
                ('m 50 50 20 20', 'm 50 50 l 20 20'),
                ((('m', (50, 50)), ('l', (20, 20))), 'm 50 50 l 20 20'),
        ):
            self._assertPath(Path(path), ret)

    def test_create_from_points(self):
        """Paths can be made of simple list of tuples"""
        arg = ((10, 10), (4, 5), (16, -9), (20, 20))
        self.assertEqual(str(Path(arg)), 'L 10 10 L 4 5 L 16 -9 L 20 20')

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

    def test_bounding_box_lines(self):
        """
        Test the bounding box calculations

        A diagonal line from 20,20 to 90,90 then to +10,+10  "\"

        """
        self.assertEqual((20, 100, 20, 100), Path('M 20,20 L 90,90 l 10,10 Z').bounding_box())
        self.assertEqual((10, 90, 10, 90), Path('M 20,20 L 90,90 L 10,10 Z').bounding_box())

    def test_bounding_box_curves(self):
        """
        Test the bounding box calculations of a curve
        """
        self.assertEqual(
            (-5.7198883, 104.71989, -5.6395306, 104.71989),
            Path('M 85,14 C 104.63953,33.639531 104.71989,65.441157'
                 ' 85,85 65.441157,104.71989 33.558843,104.71989 14,85'
                 ' -5.7198883,65.441157 -5.6395306,33.639531 14,14'
                 ' 33.639531,-5.6395306 65.360469,-5.6395306 85,14 Z').bounding_box())

    def test_bounding_box_arcs(self):
        """
        Test the bounding box calculations with arcs (currently is rough only)

        Bounding box around a circle with a radius of 50
        it should be from 0,0 -> 100, 100
        """
        path = Path('M 85.355333,14.644651 '
                     'A 50,50 0 0 1 85.355333,85.355341'
                    ' 50,50 0 0 1 14.644657,85.355341'
                    ' 50,50 0 0 1 14.644676,14.644651'
                    ' 50,50 0 0 1 85.355333,14.644651 Z')
        # This changes between computer archtecture, needs to be trimmed
        #self.assertEqual(BoundingBox((-3.94453839208415e-06, 99.99999988134624),
        #                  (-4.881549508464541, 104.88155417512705)), path.bounding_box())
        self.assertEqual(path[1].bounding_box(path[0]), (
            85.355333, 99.99999988134624, 14.644650999999998, 85.355341))
        #self.assertEqual(('ERROR'), Path('M 10 10 S 100 100 300 0').bounding_box())
        #self.assertEqual(('ERRPR'), Path('M 10 10 Q 100 100 300 0').bounding_box())

    def test_adding_to_path(self):
        """Paths can be translated using addition"""
        ret = Path('M 20,20 L 90,90 l 10,10 Z') + (50, 50)
        self._assertPath(ret, 'M 70 70 L 140 140 l 10 10 Z')

    def test_extending(self):
        """Paths can be extended using addition"""
        ret = Path('M 20 20') + Path('L 40 40 9 10')
        self.assertEqual(type(ret), Path)
        self._assertPath(ret, 'M 20 20 L 40 40 L 9 10')

        ret = Path('M 20 20') + 'C 40 40 9 10 10 10'
        self.assertEqual(type(ret), Path)
        self._assertPath(ret, 'M 20 20 C 40 40 9 10 10 10')

    def test_subtracting_from_path(self):
        """Paths can be translated using addition"""
        ret = Path('M 20,20 L 90,90 l 10,10 Z') - (10, 10)
        self._assertPath(ret, 'M 10 10 L 80 80 l 10 10 Z')

    def test_scale(self):
        """Paths can be scaled using the times operator"""
        ret = Path('M 10,10 L 30,30 C 20 20 10 10 10 10 l 10 10') * (2.5, 3)
        self._assertPath(ret, 'M 25 30 L 75 90 C 50 60 25 30 25 30 l 25 30')

        ret = Path("M 29.867708,101.68274 A 14.867708,14.867708 0 0 1 15,116.55045 14.867708,"
                   "14.867708 0 0 1 0.13229179,101.68274 14.867708,14.867708 0 0 1 15,86.815031 "
                   "14.867708,14.867708 0 0 1 29.867708,101.68274 Z")
        ret.scale(1.2, 0.8)
        self._assertPath(ret, 'M 35.8412 81.3462 A 17.8412 17.8412 0 0 1 '
                              '18 93.2404 A 17.8412 17.8412 0 0 1 0.15875 81.3462 A 17.8412 1'
                              '7.8412 0 0 1 18 69.452 A 17.8412 17.8412 0 0 1 35.8412 81.3462 Z')

    def test_absolute(self):
        """Paths can be converted to absolute"""
        ret = Path("M 100 100 l 10 10 10 10 10 10")
        self._assertPath(ret.to_absolute(), "M 100 100 L 110 110 L 120 120 L 130 130")

        ret = Path("M 100 100 h 10 10 10 v 10 10 10")
        self._assertPath(ret.to_absolute(), "M 100 100 H 110 H 120 H 130 V 110 V 120 V 130")

        ret = Path("M 150,150 a 76,55 0 1 1 283,128")
        self._assertPath(ret.to_absolute(), "M 150 150 A 76 55 0 1 1 433 278")

    def test_relative(self):
        """Paths can be converted to relative"""
        ret = Path("M 100 100 L 110 120 140 140 300 300")
        self._assertPath(ret.to_relative(), "m 100 100 l 10 20 l 30 20 l 160 160")

        ret = Path("M 150,150 A 76,55 0 1 1 433,278")
        self._assertPath(ret.to_relative(), "m 150 150 a 76 55 0 1 1 283 128")

    def test_rotate(self):
        """Paths can be rotated"""
        ret = Path("M 0.24999949,0.24999949 H 12.979167 V 12.979167 H 0.24999949 Z")
        ret.rotate(35, 0, 0)
        self._assertPath(ret, "M 0.0613938 0.348181 L 10.4885 7.64933 L 3.18737 18.0765 L -7.23976 10.7753 Z")

        ret = Path("M 0.24999949,0.24999949 H 12.979167 V 12.979167 H 0.24999949 Z")
        ret.rotate(-35, 0, 0)
        self._assertPath(ret, "M 0.348181 0.0613938 L 10.7753 -7.23976 L 18.0765 3.18737 L 7.64933 10.4885 Z")

        ret = Path("M 0.24999949,0.24999949 H 12.979167 V 12.979167 H 0.24999949 Z")
        ret.rotate(90, 10, -10)
        self._assertPath(ret, "M -0.249999 -19.75 L -0.249999 -7.02083 L -12.9792 -7.02083 L -12.9792 -19.75 Z")

        ret = Path("M 0.24999949,0.24999949 H 12.979167 V 12.979167 H 0.24999949 Z")
        ret.rotate(90)
        self._assertPath(ret, "M 12.9792 0.249999 L 12.9792 12.9792 L 0.249999 12.9792 L 0.249999 0.249999 Z")

    def test_to_arrays(self):
        """Return the full path as a bunch of arrays"""
        ret = Path("M 100 100 L 110 120 H 20 C 120 0 6 10 10 2 Z").to_arrays()
        self.assertEqual(len(ret), 5)
        self.assertEqual(ret[0][0], 'M')
        self.assertEqual(ret[1][0], 'L')
        self.assertEqual(ret[2][0], 'H')
        self.assertEqual(ret[3][0], 'C')

    def test_transform(self):
        """Transform by a whole matrix"""
        ret = Path("M 100 100 L 110 120 L 140 140 L 300 300")
        ret.transform(Transform(translate=(10, 10)))
        self.assertEqual(str(ret), 'M 110 110 L 120 130 L 150 150 L 310 310')
        ret.transform(Transform(translate=(-10, -10)))
        self.assertEqual(str(ret), 'M 100 100 L 110 120 L 140 140 L 300 300')
        ret = Path('M 5 5 H 10 V 15')
        ret.transform(Transform(rotate=-10))
        self.assertEqual(str(ret), 'M 5.79228 4.0558 L 10.5524 2.2577 L 12.9968 12.9397')
        ret = Path("M 10 10 A 50,50 0 0 1 85.355333,85.355341 L 100 0")
        ret.transform(Transform(scale=10))
        self.assertEqual(str(ret), 'M 100 100 A 50 50 0 0 1 853.553 853.553 L 1000 0')
        self.assertRaises(ValueError, PathCommand('H', 10).transform, Transform())
