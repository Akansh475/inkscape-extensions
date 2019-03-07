# coding=utf-8
"""
Test Inkex transformational logic.
"""
from inkex.transforms import BoundingBox, Scale, Transform
from tests.base import TestCase


class TransformTest(TestCase):
    """Test transformation API and calculations"""

    def test_new_empty(self):
        """Create a transformation from two triplets matrix"""
        self.assertEqual(Transform(), ((1, 0, 0), (0, 1, 0)))

    def test_new_from_triples(self):
        """Create a transformation from two triplets matrix"""
        self.assertEqual(Transform(((1, 2, 3), (4, 5, 6))), ((1, 2, 3), (4, 5, 6)))

    def test_new_from_sextlet(self):
        """Create a transformation from a list of six numbers"""
        self.assertEqual(Transform((1, 2, 3, 4, 5, 6)), ((1, 3, 5), (2, 4, 6)))

    def test_new_from_matrix_str(self):
        """Create a transformation from a list of six numbers"""
        self.assertEqual(Transform('matrix(1, 2, 3, 4, 5, 6)'), ((1, 3, 5), (2, 4, 6)))

    def test_new_from_scale(self):
        """Create a scale based transformation"""
        self.assertEqual(Transform('scale(10)'), ((10, 0, 0), (0, 10, 0)))
        self.assertEqual(Transform('scale(10, 3.3)'), ((10, 0, 0), (0, 3.3, 0)))

    def test_new_from_translate(self):
        """Create a translate transformation"""
        self.assertEqual(Transform('translate(12)'), ((1, 0, 12), (0, 1, 0)))
        self.assertEqual(Transform('translate(12, 14)'), ((1, 0, 12), (0, 1, 14)))

    def test_new_from_rotate(self):
        """Create a rotational transformation"""
        self.assertEqual(str(Transform('rotate(90)')),
                         'matrix(6.12323e-17 1 -1 6.12323e-17 0 0)')
        self.assertEqual(str(Transform('rotate(90 10 12)')),
                         'matrix(6.12323e-17 1 -1 6.12323e-17 22 2)')

    def test_new_from_skew(self):
        """Create skew x/y transformations"""
        self.assertEqual(str(Transform('skewX(10)')), 'matrix(1 0 0.176327 1 0 0)')
        self.assertEqual(str(Transform('skewY(10)')), 'matrix(1 0.176327 0 1 0 0)')

    def test_invalid_creation_string(self):
        """Test creating invalid transforms"""
        self.assertEqual(Transform('boo(4)'), ((1, 0, 0), (0, 1, 0)))

    def test_invalid_creation_matrix(self):
        """Test creating invalid transforms"""
        self.assertRaises(ValueError, Transform, 0.0)
        self.assertRaises(ValueError, Transform, (0.0,))
        self.assertRaises(ValueError, Transform, (0.0, 0.0, 0.0))

    def test_repr(self):
        """Test repr string"""
        self.assertEqual(repr(Transform()), 'Transform(((1, 0, 0), (0, 1, 0)))')

    def test_matrix_inversion(self):
        """Test the negative of a transformation"""
        self.assertEqual(-Transform('rotate(45)'), Transform('rotate(-45)'))
        self.assertEqual(-Transform('translate(12, 10)'), Transform('translate(-12, -10)'))
        self.assertEqual(-Transform('scale(4)'), Transform('scale(0.25)'))

    def test_apply_to_point(self):
        """Test applying the transformation to a point"""
        trans = Transform('translate(10, 10)')
        self.assertEqual(trans.apply_to_point((10, 10)), (20, 20))
        self.assertRaises(ValueError, trans.apply_to_point, '')


class ScaleTest(TestCase):
    """Test scale class"""

    def test_creation(self):
        """Creating scales"""
        self.assertEqual(Scale(), (None, None))
        self.assertEqual(Scale(1), (1, 1))
        self.assertEqual(Scale(10), (10, 10))
        self.assertEqual(Scale(10, 20), (10, 20))
        self.assertEqual(Scale(10, 2, 100, 1, 4), (1, 100))
        self.assertEqual(Scale([2, 50]), (2, 50))
        self.assertEqual(Scale([5, 50], [4, 5]), (4, 50))

    def test_center(self):
        """Center of a scale"""
        self.assertEqual(Scale().center(), None)
        self.assertEqual(Scale(0, 10).center(), 5)
        self.assertEqual(Scale(-10, 10).center(), 0)


class BoundingBoxTest(TestCase):
    """Test bounding box calculations"""

    def test_bbox_sum(self):
        """Test adding bboxes together"""
        self.assertEqual(BoundingBox([0, 10, 0, 10]) + (-10, 0, -10, 0), (-10, 10, -10, 10))
        ret = sum([
            BoundingBox([-5, 0, 0, 0]),
            BoundingBox([0, 5, 0, 0]),
            BoundingBox([0, 0, -5, 0]),
            BoundingBox([0, 0, 0, 5])])
        self.assertEqual(ret, (-5, 5, -5, 5))

    # def setUp(self):
    #    args = [self.data_file('svg', 'simpletransform.test.svg')]
    #    self.e = Effect()
    #    self.e.affect(args, False)

    # def test_scaled_object(self):
    #    "Object in the defs with 50,50 scaled by 0.5 when used"
    #    bbox = computeBBox(self.e.document.xpath("//svg:g", namespaces=NSS))
    #    text_bbox = "{} {} {} {}".format(bbox[0], bbox[1], bbox[2], bbox[3])
    #    self.assertEqual("0.0 25.0 0.0 25.0", text_bbox)
