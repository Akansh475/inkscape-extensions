# coding=utf-8
"""
Test Inkex transformational logic.
"""
from inkex.transforms import (
    BoundingBox, Scale, Transform, TranslateTransform, ScaleTransform, RotateTransform, DirectedLineSegment
)
from inkex.tester import TestCase

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

    def test_translate(self):
        """Test making translate specific items"""
        self.assertEqual(str(TranslateTransform(10.6, 99.9)), "translate(10.6, 99.9)")

    def test_scale(self):
        """Test making scale specific items"""
        self.assertEqual(str(ScaleTransform(1.0, 2.2)), "scale(1, 2.2)")

    def test_rotate(self):
        """Test making rotate specific items"""
        self.assertEqual(str(RotateTransform(45, 10, 10)), "matrix(0.707107 0.707107 -0.707107 0.707107 10 -4.14214)")

    def test_add_transform(self):
        """Quickly add known transforms"""
        tr = Transform()
        tr.add_scale(5.0, 1.0)
        self.assertEqual(str(tr), 'scale(5, 1)')
        tr.add_translate(10, 10)
        self.assertEqual(str(tr), 'matrix(5 0 0 1 50 10)')


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
        self.assertEqual(repr(Scale([5, 10])), 'scale:(5, 10)')

    def test_center(self):
        """Center of a scale"""
        self.assertEqual(Scale().center, None)
        self.assertEqual(Scale(0, 10).center, 5)
        self.assertEqual(Scale(-10, 10).center, 0)

    def test_size(self):
        """Size of the scale"""
        self.assertEqual(Scale().size, None)
        self.assertEqual(Scale(10, 30).size, 20)
        self.assertEqual(Scale(-10, 10).size, 20)
        self.assertEqual(Scale(-30, -10).size, 20)

    def test_combine(self):
        """Combine scales together"""
        self.assertEqual(Scale(9, 10) + Scale(4, 5), (4, 10))
        self.assertEqual(sum([Scale(4), Scale(3), Scale(10)]), (3, 10))
        self.assertEqual(Scale(2, 2) * 2, (4, 4))

    def test_errors(self):
        """Expected errors"""
        self.assertRaises(ValueError, Scale, 'foo')

class BoundingBoxTest(TestCase):
    """Test bounding box calculations"""
    def test_bbox(self):
        """Creating bounding boxes"""
        self.assertEqual(BoundingBox((15)), (15, 15, None, None))
        self.assertEqual(BoundingBox(1, 3), (1, 1, 3, 3))
        self.assertEqual(BoundingBox((1, 3)), (1, 1, 3, 3))
        self.assertEqual(BoundingBox((1, 2), (3, 4)), (1, 2, 3, 4))
        self.assertEqual(BoundingBox(((1, 2), (3, 4))), (1, 3, 2, 4))
        self.assertEqual(BoundingBox((1, 2, 3, 4)), (1, 2, 3, 4))
        self.assertEqual(repr(BoundingBox((1, 2, 3, 4))), 'BoundingBox((1, 2, 3, 4))')

    def test_bbox_sum(self):
        """Test adding bboxes together"""
        self.assertEqual(BoundingBox([0, 10, 0, 10]) + (-10, 0, -10, 0), (-10, 10, -10, 10))
        ret = sum([
            BoundingBox([-5, 0, 0, 0]),
            BoundingBox([0, 5, 0, 0]),
            BoundingBox([0, 0, -5, 0]),
            BoundingBox([0, 0, 0, 5])])
        self.assertEqual(ret, (-5, 5, -5, 5))
        self.assertEqual((-10, 2) + ret, (-10, 5, -5, 5))
        self.assertEqual(ret + (1, -10), (-5, 5, -10, 5))

    def test_bbox_scale(self):
        """Bounding Boxes can be scaled"""
        self.assertEqual(BoundingBox(1, 3) * 2, (2, 2, 6, 6))

class SegmentTest(TestCase):
    """Test special Segments"""
    def test_segment_creation(self):
        """Test segments"""
        self.assertEqual(DirectedLineSegment((1, 2), (3, 4)), (1, 3, 2, 4))
        self.assertEqual(repr(DirectedLineSegment((1, 2), (3, 4))), 'DirectedLineSegment(((1, 2), (3, 4)))')

    def test_segment_maths(self):
        """Segments have calculations"""
        self.assertEqual(DirectedLineSegment((0, 0), (10, 0)).angle, 0)
