# coding=utf-8
"""
Test Inkex transformational logic.
"""
from inkex.transforms import (
    Vector2d, BoundingBox, Scale, Transform, TranslateTransform,
    ScaleTransform, RotateTransform, DirectedLineSegment
)
from inkex.tester import TestCase

class Vector2dTest(TestCase):
    """Test the Vector2d object"""
    def test_vector_creation(self):
        """Test Vector2D creation"""
        vec0 = Vector2d(15, 22)
        self.assertEqual(vec0.x, 15)
        self.assertEqual(vec0.y, 22)

        vec1 = Vector2d()
        self.assertEqual(vec1.x, 0)
        self.assertEqual(vec1.y, 0)

        vec2 = Vector2d((17, 32))
        self.assertEqual(vec2.x, 17)
        self.assertEqual(vec2.y, 32)

        vec3 = Vector2d(vec0)
        self.assertEqual(vec3.x, 15)
        self.assertEqual(vec3.y, 22)

        self.assertRaises(ValueError, Vector2d, (1))
        self.assertRaises(ValueError, Vector2d, (1, 2, 3))

    def test_binary_operators(self):
        """Test binary operators for vector2d"""
        vec1 = Vector2d(15, 22)
        vec2 = Vector2d(5, 3)

        self.assertTrue((vec1 - vec2).is_close((10, 19)))
        self.assertTrue((vec1 - (5, 3)).is_close((10, 19)))
        self.assertTrue(((15, 22) - vec2).is_close((10, 19)))
        self.assertTrue((vec1 + vec2).is_close((20, 25)))
        self.assertTrue((vec1 + (5, 3)).is_close((20, 25)))
        self.assertTrue(((15, 22) + vec2).is_close((20, 25)))
        self.assertTrue((vec1 * 2).is_close((30, 44)))
        self.assertTrue((2 * vec1).is_close((30, 44)))
        self.assertTrue((vec1 / 2).is_close((7.5, 11)))
        self.assertTrue((vec1.__div__(2)).is_close((7.5, 11)))
        self.assertTrue((vec1 // 2).is_close((7.5, 11)))

    def test_ioperators(self):
        """Test operators for vector2d"""
        vec = Vector2d(15, 22)
        vec += (1, 1)
        self.assertTrue(vec.is_close((16, 23)))
        vec -= (10, 20)
        self.assertTrue(vec.is_close((6, 3)))
        vec *= 5
        self.assertTrue(vec.is_close((30, 15)))
        vec /= 90
        self.assertTrue(vec.is_close((1.0/3, 1.0/6)))
        vec //= 1.0/3
        self.assertTrue(vec.is_close((1, 0.5)))

    def test_unary_operators(self):
        """Test unary operators"""
        vec = Vector2d(1, 2)
        self.assertTrue((-vec).is_close((-1, -2)))
        self.assertTrue((+vec).is_close(vec))
        self.assertTrue(+vec is not vec)  # returned value is a copy

    def test_representations(self):
        """Test Vector2D Repr"""
        self.assertEqual(str(Vector2d(1, 2)), "1, 2")
        self.assertEqual(repr(Vector2d(1, 2)), "Vector2d(1, 2)")
        self.assertEqual(Vector2d(1, 2).to_tuple(), (1, 2))

    def test_assign(self):
        """Test vector2d assignement"""
        vec = Vector2d(10, 20)
        vec.assign(5, 10)
        self.assertAlmostTuple(vec, (5, 10))
        vec.assign((7, 11))
        self.assertAlmostTuple(vec, (7, 11))

    def test_getitem(self):
        """Test getitem for Vector2D"""
        vec = Vector2d(10, 20)
        self.assertEqual(len(vec), 2)
        self.assertEqual(vec[0], 10)
        self.assertEqual(vec[1], 20)


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
        self.assertEqual(str(Transform('rotate(90)')), 'rotate(90)')
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
        self.assertEqual(trans.apply_to_point((10, 10)).to_tuple(), (20, 20))
        self.assertRaises(ValueError, trans.apply_to_point, '')

    def test_translate(self):
        """Test making translate specific items"""
        self.assertEqual(str(TranslateTransform(10.6, 99.9)), "translate(10.6, 99.9)")

    def test_scale(self):
        """Test making scale specific items"""
        self.assertEqual(str(ScaleTransform(1.0, 2.2)), "scale(1, 2.2)")

    def test_rotate(self):
        """Test making rotate specific items"""
        self.assertEqual(str(RotateTransform(45)), "rotate(45)")
        self.assertEqual(str(RotateTransform(45, 10, 10)), "matrix(0.707107 0.707107 -0.707107 0.707107 10 -4.14214)")

    def test_combine(self):
        """Test combining transformations"""
        self.assertEqual(str(Transform(scale=2.0, translate=(5, 6))), 'matrix(2 0 0 2 5 6)')
        self.assertEqual(str(Transform(scale=2.0, rotate=45)), 'matrix(1.41421 1.41421 -1.41421 1.41421 0 0)')

    def test_add_transform(self):
        """Quickly add known transforms"""
        tr = Transform()
        tr.add_scale(5.0, 1.0)
        self.assertEqual(str(tr), 'scale(5, 1)')
        tr.add_translate(10, 10)
        self.assertEqual(str(tr), 'matrix(5 0 0 1 50 10)')

    def test_is_unity(self):
        unity = Transform()
        self.assertTrue(unity.is_rotate())
        self.assertTrue(unity.is_scale())
        self.assertTrue(unity.is_translate())

    def test_is_rotation(self):
        r1 = Transform(rotate=21)
        r2 = Transform(rotate=35)
        r3 = Transform(rotate=53)

        self.assertFalse(Transform(translate=1e-9).is_rotate(exactly=True))
        self.assertFalse(Transform(scale=1+1e-9).is_rotate(exactly=True))
        self.assertFalse(Transform(skewx=1e-9).is_rotate(exactly=True))
        self.assertFalse(Transform(skewy=1e-9).is_rotate(exactly=True))

        self.assertTrue(Transform(translate=1e-9).is_rotate(exactly=False))
        self.assertTrue(Transform(scale=1+1e-9).is_rotate(exactly=False))
        self.assertTrue(Transform(skewx=1e-9).is_rotate(exactly=False))
        self.assertTrue(Transform(skewy=1e-9).is_rotate(exactly=False))

        self.assertTrue(r1.is_rotate())
        self.assertTrue(r2.is_rotate())
        self.assertTrue(r3.is_rotate())

        self.assertFalse(r1.is_translate())
        self.assertFalse(r2.is_translate())
        self.assertFalse(r3.is_translate())

        self.assertFalse(r1.is_scale())
        self.assertFalse(r2.is_scale())
        self.assertFalse(r3.is_scale())

        self.assertTrue((r1 * r1).is_rotate())
        self.assertTrue((r1 * r2).is_rotate())
        self.assertTrue((r1 * r2 * r3 * r2 * r1).is_rotate())

    def test_is_translate(self):
        from math import sqrt, pi
        t1 = Transform(translate=(1.1,))
        t2 = Transform(translate=(1.3, 2.7))
        t3 = Transform(translate=(sqrt(2) / 2, pi))

        self.assertFalse(Transform(rotate=1e-9).is_translate(exactly=True))
        self.assertFalse(Transform(scale=1+1e-9).is_translate(exactly=True))
        self.assertFalse(Transform(skewx=1e-9).is_translate(exactly=True))
        self.assertFalse(Transform(skewy=1e-9).is_translate(exactly=True))

        self.assertTrue(Transform(rotate=1e-9).is_translate(exactly=False))
        self.assertTrue(Transform(scale=1+1e-9).is_translate(exactly=False))
        self.assertTrue(Transform(skewx=1e-9).is_translate(exactly=False))
        self.assertTrue(Transform(skewy=1e-9).is_translate(exactly=False))

        self.assertTrue(t1.is_translate())
        self.assertTrue(t2.is_translate())
        self.assertTrue(t3.is_translate())
        self.assertFalse(t1.is_rotate())
        self.assertFalse(t2.is_rotate())
        self.assertFalse(t3.is_rotate())
        self.assertFalse(t1.is_scale())
        self.assertFalse(t2.is_scale())
        self.assertFalse(t3.is_scale())

        self.assertTrue((t1 * t1).is_translate())
        self.assertTrue((t1 * t2).is_translate())
        self.assertTrue((t1 * t2 * t3 * t2 * t1).is_translate())
        self.assertFalse(t1 * t2 * t3 * -t1 * -t2 * -t3)  # is almost unity

    def test_is_scale(self):
        from math import sqrt, pi

        s1 = Transform(scale=(1.1,))
        s2 = Transform(scale=(1.3, 2.7))
        s3 = Transform(scale=(sqrt(2) / 2, pi))

        self.assertFalse(Transform(translate=1e-9).is_scale(exactly=True))
        self.assertFalse(Transform(rotate=1e-9).is_scale(exactly=True))
        self.assertFalse(Transform(skewx=1e-9).is_scale(exactly=True))
        self.assertFalse(Transform(skewy=1e-9).is_scale(exactly=True))

        self.assertTrue(Transform(translate=1e-9).is_scale(exactly=False))
        self.assertTrue(Transform(rotate=1e-9).is_scale(exactly=False))
        self.assertTrue(Transform(skewx=1e-9).is_scale(exactly=False))
        self.assertTrue(Transform(skewy=1e-9).is_scale(exactly=False))

        self.assertFalse(s1.is_translate())
        self.assertFalse(s2.is_translate())
        self.assertFalse(s3.is_translate())
        self.assertFalse(s1.is_rotate())
        self.assertFalse(s2.is_rotate())
        self.assertFalse(s3.is_rotate())
        self.assertTrue(s1.is_scale())
        self.assertTrue(s2.is_scale())
        self.assertTrue(s3.is_scale())

    def test_rotation_degrees(self):
        self.assertAlmostEqual(Transform(rotate=30).rotation_degrees(), 30)
        self.assertAlmostEqual(Transform(translate=(10, 20)).rotation_degrees(), 0)
        self.assertAlmostEqual(Transform(scale=(1, 1)).rotation_degrees(), 0)

        self.assertAlmostEqual(Transform(rotate=35, translate=(10, 20)).rotation_degrees(), 35)
        self.assertAlmostEqual(Transform(rotate=35, translate=(10, 20), scale=5).rotation_degrees(), 35)
        self.assertAlmostEqual(Transform(rotate=35, translate=(10, 20), scale=(5, 5)).rotation_degrees(), 35)

        def rotation_degrees(**kwargs):
            return Transform(**kwargs).rotation_degrees()

        self.assertRaises(ValueError, rotation_degrees, rotate=35, skewx=1)
        self.assertRaises(ValueError, rotation_degrees, rotate=35, skewy=1)
        self.assertRaises(ValueError, rotation_degrees, rotate=35, scale=(10, 11))
        self.assertRaises(ValueError, rotation_degrees, rotate=35, scale=(10, 11))

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
        self.assertEqual(repr(DirectedLineSegment((1, 2), (3, 4))), 'DirectedLineSegment((1, 2), (3, 4))')

    def test_segment_maths(self):
        """Segments have calculations"""
        self.assertEqual(DirectedLineSegment((0, 0), (10, 0)).angle, 0)


class ExtremaTest(TestCase):
    """Test school formula implementation"""

    def test_cubic_extrema_1(self):
        from inkex.transforms import cubic_extrema
        a, b, c, d = 14.644651000000003194,-4.881549508464541276,-4.8815495084645448287,14.644651000000003194
        cmin, cmax = cubic_extrema(a, b, c, d)
        self.assertAlmostEqual(cmin, 0, delta=1e-6)
        self.assertAlmostEqual(cmax, a, delta=1e-6)

    def test_quadratic_extrema_1(self):
        from inkex.transforms import quadratic_extrema
        a, b = 5.0, 12.0
        cmin, cmax = quadratic_extrema(a, b, a)
        self.assertAlmostEqual(cmin, 5, delta=1e-6)
        self.assertAlmostEqual(cmax, 8.5, delta=1e-6)

    def test_quadratic_extrema_2(self):
        from inkex.transforms import quadratic_extrema
        a = 5.0
        cmin, cmax = quadratic_extrema(a,a,a)
        self.assertAlmostEqual(cmin, a, delta=1e-6)
        self.assertAlmostEqual(cmax, a, delta=1e-6)
