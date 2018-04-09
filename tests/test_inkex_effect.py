#!/usr/bin/env python

import os
import tempfile

from tests.base import TestCase, test_support

from inkex.effect import Effect


class GetDocumentWidthTest(TestCase):
    """Tests for Effect.getDocumentWidth()."""

    def test_no_dimensions(self):
        e = new_effect_with_svg_attrs('')
        self.assertEqual(e.getDocumentWidth(), '0')

    def test_empty_width(self):
        # An empty width value should be the same as a missing width.
        e = new_effect_with_svg_attrs('width=""')
        self.assertEqual(e.getDocumentWidth(), '0')

    def test_empty_viewBox(self):
        # An empty viewBox value should be the same as a missing viewBox.
        e = new_effect_with_svg_attrs('viewBox=""')
        self.assertEqual(e.getDocumentWidth(), '0')

    def test_empty_width_and_empty_viewBox(self):
        # Empty values for both should be the same as both missing.
        e = new_effect_with_svg_attrs('width="" viewBox=""')
        self.assertEqual(e.getDocumentWidth(), '0')

    def test_width_only(self):
        e = new_effect_with_svg_attrs('width="120mm"')
        self.assertEqual(e.getDocumentWidth(), '120mm')

    def test_width_and_viewBox(self):
        # If both are present, width overrides viewBox.
        e = new_effect_with_svg_attrs('width="120mm" viewBox="0 0 22 99"')
        self.assertEqual(e.getDocumentWidth(), '120mm')

    def test_viewBox_only(self):
        e = new_effect_with_svg_attrs('viewBox="0 0 22 99"')
        self.assertEqual(e.getDocumentWidth(), '22')

    def test_empty_width_and_valid_viewBox(self):
        # An empty width value should be the same as a missing width.
        e = new_effect_with_svg_attrs('width="" viewBox="0 0 22 99"')
        self.assertEqual(e.getDocumentWidth(), '22')

    def test_non_zero_viewBox_x_has_no_effect(self):
        # Demonstrate that a non-zero x value (viewbox[0]) does not affect the
        # width value.
        e = new_effect_with_svg_attrs('width="" viewBox="5 7 22 99"')
        self.assertEqual(e.getDocumentWidth(), '22')


class GetDocumentHeightTest(TestCase):
    """Tests for Effect.getDocumentHeight()."""

    def test_no_dimensions(self):
        e = new_effect_with_svg_attrs('')
        self.assertEqual(e.getDocumentHeight(), '0')

    def test_empty_height(self):
        # An empty height value should be the same as a missing height.
        e = new_effect_with_svg_attrs('height=""')
        self.assertEqual(e.getDocumentHeight(), '0')

    def test_empty_viewBox(self):
        # An empty viewBox value should be the same as a missing viewBox.
        e = new_effect_with_svg_attrs('viewBox=""')
        self.assertEqual(e.getDocumentHeight(), '0')

    def test_empty_height_and_empty_viewBox(self):
        # Empty values for both should be the same as both missing.
        e = new_effect_with_svg_attrs('height="" viewBox=""')
        self.assertEqual(e.getDocumentHeight(), '0')

    def test_height_only(self):
        e = new_effect_with_svg_attrs('height="330px"')
        self.assertEqual(e.getDocumentHeight(), '330px')

    def test_height_and_viewBox(self):
        # If both are present, height overrides viewBox.
        e = new_effect_with_svg_attrs('height="330px" viewBox="0 0 22 99"')
        self.assertEqual(e.getDocumentHeight(), '330px')

    def test_viewBox_only(self):
        e = new_effect_with_svg_attrs('viewBox="0 0 22 99"')
        self.assertEqual(e.getDocumentHeight(), '99')

    def test_empty_height_and_valid_viewBox(self):
        # An empty height value should be the same as a missing height.
        e = new_effect_with_svg_attrs('height="" viewBox="0 0 22 99"')
        self.assertEqual(e.getDocumentHeight(), '99')

    def test_non_zero_viewBox_y_has_no_effect(self):
        # Demonstrate that a non-zero y value (viewbox[1]) does not affect the
        # height value.
        e = new_effect_with_svg_attrs('height="" viewBox="5 7 22 99"')
        self.assertEqual(e.getDocumentHeight(), '99')


class GetDocumentUnitTest(TestCase):
    """Tests for Effect.getDocumentUnit()."""

    def test_no_dimensions(self):
        e = new_effect_with_svg_attrs('')
        self.assertEqual(e.getDocumentUnit(), 'px')

    def test_width_only(self):
        e = new_effect_with_svg_attrs('width="100mm"')
        # TODO: Determine whether returning 'px' in this case is the
        #     intended behavior.
        self.assertEqual(e.getDocumentUnit(), 'px')

    def test_height_only(self):
        e = new_effect_with_svg_attrs('height="100mm"')
        # TODO: Determine whether returning 'px' in this case is the
        #     intended behavior.
        self.assertEqual(e.getDocumentUnit(), 'px')

    def test_viewBox_only(self):
        e = new_effect_with_svg_attrs('viewBox="0 0 377 565"')
        self.assertEqual(e.getDocumentUnit(), 'px')

    # Unit-ratio tests. Don't exhaustively test every unit conversion, just
    # demonstrate that the logic works.

    def test_width_and_viewBox_px(self):
        # 100mm is ~377px, so unit should be 'px'.
        e = new_effect_with_svg_attrs('width="100mm" viewBox="0 0 377 565"')
        self.assertEqual(e.getDocumentUnit(), 'px')

    def test_width_and_viewBox_in(self):
        # 100mm is ~3.94in, so unit should be 'in'.
        e = new_effect_with_svg_attrs('width="100mm" viewBox="0 0 3.94 5.90"')
        self.assertEqual(e.getDocumentUnit(), 'in')

    def test_unitless_width_and_viewBox(self):
        # Unitless width should be treated as 'px'.
        # 3779px is ~1m, so unit should be 'm'.
        e = new_effect_with_svg_attrs('width="3779" viewBox="0 0 1 1.5"')
        self.assertEqual(e.getDocumentUnit(), 'm')

    def test_height_ignored_with_viewBox(self):
        # 150mm is ~5.90in, so unit should be 'in', but since height is ignored
        # the returned unit will be 'px'.
        # TODO: Determine whether returning 'px' in this case is the intended
        #     behavior.
        e = new_effect_with_svg_attrs('height="150mm" viewBox="0 0 3.94 5.90"')
        self.assertEqual(e.getDocumentUnit(), 'px')

    def test_height_width_and_viewBox(self):
        # 100mm is ~23.6pc, so unit should be 'pc'.
        e = new_effect_with_svg_attrs(
                'width="100mm" height="150mm" viewBox="0 0 23.6 35.4"')
        self.assertEqual(e.getDocumentUnit(), 'pc')

    def test_large_error_reverts_to_px(self):
        # 100mm is ~23.6pc; 24.1 is ~2% off from that, so unit should fall back
        # to 'px' instead of using the closest match 'pc'.
        e = new_effect_with_svg_attrs('width="100mm" viewBox="0 0 24.1 35.4"')
        self.assertEqual(e.getDocumentUnit(), 'px')

    # Width-parsing tests.

    def test_width_number_parsing(self):
        widths = (
            '100mm',
            '100  mm',
            '   100mm',
            # TODO: Allow whitespace after the units and add a test case.
            #     Currently, '100mm  ' would fail here, because the units will
            #     be treated as 'px'.
            '+100mm',
            '100.0mm',
            '100.0e0mm',
            '10.0e1mm',
            '10.0e+1mm',
            '1000.0e-1mm',
            '.1e+3mm',
            '+.1e+3mm',
        )
        for w in widths:
            # 100mm is ~3.94in, so unit should be 'in'.
            svg = 'width="{}" viewBox="0 0 3.94 5.90"'.format(w)
            e = new_effect_with_svg_attrs(svg)
            actual = e.getDocumentUnit()
            expected = 'in'
            self.assertEqual(
                    actual, expected,
                    msg='{} should be {} for [{}]'.format(actual, expected, w))

    # TODO: Demonstrate that unknown width units are treated as px while
    #     determining the ratio.

    # 100px fallback tests. Although that value is an arbitrary default, it's
    # possible for users of inkex.Effect to depend on this behavior.
    # NOTE: Do not treat the existence of these tests as a reason to preserve
    # the 100px fallback logic.

    def test_bad_width_number_defaults_to_100(self):
        # First, demonstrate that 1in is 2.54cm, so unit should be 'cm'.
        e = new_effect_with_svg_attrs('width="1in" viewBox="0 0 2.54 1"')
        self.assertEqual(e.getDocumentUnit(), 'cm')

        # Corrupt the width to contain an invalid number component; note that
        # the units change to 'm'. This is because the corrupt number part is
        # replaced with 100 while the unit is preserved, producing a width of
        # "100in"; 100in is 2.54m.
        e = new_effect_with_svg_attrs('width="ABCDin" viewBox="0 0 2.54 1"')
        self.assertEqual(e.getDocumentUnit(), 'm')

    def test_bad_viewbox_entry_defaults_to_100px(self):
        # First, demonstrate that 3779px is 1m, so unit should be 'm'.
        e = new_effect_with_svg_attrs('width="3779px" viewBox="0 0 1 1"')
        self.assertEqual(e.getDocumentUnit(), 'm')

        # Corrupt the viewBox to include a non-float value; note that
        # the units change to 'cm'. This is because the corrupt viewBox
        # is effectively replaced with "0 0 100 100"; 3779/100 == 37.79,
        # and 37.79px is 1cm.
        # Also note that the corruption did not touch the width element
        # of the viewBox; this fallback happens if any element is corrupt.
        e = new_effect_with_svg_attrs('width="3779px" viewBox="x 0 1 1"')
        self.assertEqual(e.getDocumentUnit(), 'cm')


class UserUnitTest(TestCase):
    """Tests for methods that are based on the value of getDocumentUnit()."""

    def new_effect_with_uu(self, unit):
        """Returns an Effect e where e.getDocumentUnit() == unit."""
        # Effect bases its "user unit" on the ratio between the SVG width and
        # the width of the viewBox (viewBox[2]).
        svg = 'width="1{}" viewBox="0 0 1 1"'.format(unit)
        e = new_effect_with_svg_attrs(svg)
        # Demonstrate that this helper does the right thing.
        self.assertEqual(e.getDocumentUnit(), unit, msg=svg)
        return e

    #
    # Effect.unittouu() tests
    #

    # Unit-ratio tests. Don't exhaustively test every unit conversion, just
    # demonstrate that the logic works.

    def test_unittouu_in_to_cm(self):
        e = self.new_effect_with_uu('cm')
        # 1in is ~2.54cm
        self.assertAlmostEqual(e.unittouu('1in'), 2.54)

    def test_unittouu_yd_to_m(self):
        e = self.new_effect_with_uu('m')
        # 1yd is ~0.9144m
        self.assertAlmostEqual(e.unittouu('1yd'), 0.9144)

    def test_unittouu_identity(self):
        e = self.new_effect_with_uu('pc')
        # If the input and output units are the same, the input and output
        # values should exactly be the same, too.
        self.assertEqual(e.unittouu('9.87654321pc'), 9.87654321)

    def test_unittouu_unitless_input_defaults_to_px(self):
        e = self.new_effect_with_uu('in')
        # Passing a unitless value to unittouu() should treat the units as 'px'.
        # 1in == 96px
        self.assertEqual(e.unittouu('96'), 1)

    def test_unittouu_empty_input_defaults_to_zero(self):
        e = self.new_effect_with_uu('in')
        # Passing an empty string to unittouu() should treat the value as zero.
        self.assertEqual(e.unittouu(''), 0)

    def test_unittouu_input_number_parsing(self):
        inputs = (
            '100pc',
            '100  pc',
            # TODO: Allow whitespace before the value and add a test case.
            #     Currently, '  100pc' would fail here, because the value will
            #     be treated as 0.0.
            # TODO: Allow whitespace after the units and add a test case.
            #     Currently, '100pc  ' would fail here, because the units will
            #     be treated as 'px'.
            '+100pc',
            '100.0pc',
            '100.0e0pc',
            '10.0e1pc',
            '10.0e+1pc',
            '1000.0e-1pc',
            '.1e+3pc',
            '+.1e+3pc',
        )
        e = self.new_effect_with_uu('px')
        for i in inputs:
            # 100pc is ~3.937in
            actual = e.unittouu(i)
            expected = 1600
            self.assertEqual(
                    actual, expected,
                    msg='{} should be {} for [{}]'.format(actual, expected, i))

    # Malformed input tests.

    def test_unittouu_bad_input_number_defaults_to_zero(self):
        e = self.new_effect_with_uu('cm')
        # Demonstrate that 1in is ~2.54cm.
        self.assertAlmostEqual(e.unittouu('1in'), 2.54)

        # Corrupt the input to contain an invalid number component; note that
        # the result changes to zero.
        self.assertEqual(e.unittouu('ABCDin'), 0)

    def test_unittouu_bad_input_unit_defaults_to_px(self):
        e = self.new_effect_with_uu('in')
        # Demonstrate that 1.0in passes through without change.
        self.assertAlmostEqual(e.unittouu('1.0in'), 1.0)

        # Corrupt the input to contain an invalid unit component; note that the
        # result changes 1/96, the ratio between inches and pixels. This is
        # because unittouu() treats unknown units as 'px'.
        self.assertAlmostEqual(e.unittouu('1.0ABCD'), 1/96.0)

    #
    # Effect.uutounit() tests
    #

    # Unit-ratio tests. Don't exhaustively test every unit conversion, just
    # demonstrate that the logic works.

    def test_uutounit_cm_to_in(self):
        e = self.new_effect_with_uu('in')
        # Convert 1 user unit ('in') to 'cm'.
        # 1in is ~2.54cm
        self.assertAlmostEqual(e.uutounit(1, 'cm'), 2.54)

    def test_uutounit_m_to_yd(self):
        e = self.new_effect_with_uu('yd')
        # Convert 1 user unit ('yd') to 'm'.
        # 1yd is ~0.9144m
        self.assertAlmostEqual(e.uutounit(1, 'm'), 0.9144)

    def test_uutounit_identity(self):
        e = self.new_effect_with_uu('pc')
        # If the input and output units are the same, the input and output
        # values should exactly be the same, too.
        self.assertEqual(e.uutounit(9.87654321, 'pc'), 9.87654321)

    # Failure tests.

    def test_uutounit_unknown_unit_raises(self):
        e = self.new_effect_with_uu('in')
        # Demonstrate that passing an unknown unit string to uutounit()
        # raises an exception.
        # TODO: Determine whether this is the right behavior; none of the other
        #     unit-related methods raises errors on bad units, they treat them
        #     as 'px'. It would be better for them all to be consistent, either
        #     by silently converting to 'px' here or by raising exceptions in
        #     the other methods.
        self.assertRaises(Exception, e.uutounit, 1, 'xy')

    #
    # Effect.addDocumentUnit() tests
    #

    def test_addDocumentUnit_common(self):
        # For valid float inputs, the output should be the input with
        # the user unit appended.
        e = self.new_effect_with_uu('pt')
        cases = (
            # Input, expected output
            ('100', '100pt'),
            ('+100', '+100pt'),
            ('100.0', '100.0pt'),
            ('100.0e0', '100.0e0pt'),
            ('10.0e1', '10.0e1pt'),
            ('10.0e+1', '10.0e+1pt'),
            ('1000.0e-1', '1000.0e-1pt'),
            ('.1e+3', '.1e+3pt'),
            ('+.1e+3', '+.1e+3pt'),

            # Demonstrate whitespace-preserving behavior.
            # TODO: Determine whether this is expected; consider stripping
            #     whitespace and updating these tests.
            ('   100', '   100pt'),
            ('100   ', '100   pt'),
            ('  100   ', '  100   pt'),
        )
        for input_value, expected in cases:
            self.assertEqual(e.addDocumentUnit(input_value), expected)

    def test_addDocumentUnit_non_float_strings_pass_through(self):
        # Strings that are invalid floats should pass through unchanged.
        inputs = (
            '',
            'ABCD',
            '.',
            '   ',
        )
        e = self.new_effect_with_uu('pt')
        for i in inputs:
            self.assertEqual(e.addDocumentUnit(i), i)

    def test_addDocumentUnit_float_type_raises(self):
        # addDocumentUnit() expects a string. Demonstrate that passing
        # an actual float value raises an exception.
        # TODO: Determine whether this is the desired behavior. If so,
        #     consider changing addDocumentUnit() to handle the case more
        #     explicitly.
        e = self.new_effect_with_uu('pt')
        self.assertRaises(Exception, e.addDocumentUnit, 1.2)


def new_effect_with_svg_attrs(svg_attrs):
    """Returns an Effect based on a simple SVG element.

    Args:
       svg_attrs: A string containing attributes to add to the
           root <svg> element of a minimal SVG document.
    Returns: An Effect object.
    """
    svg = ('<?xml version="1.0" encoding="UTF-8" standalone="no"?>'
           '<svg {}></svg>'.format(svg_attrs))
    return new_test_effect(svg)


# TODO: Consider moving this into base/__init__.py. Allow overriding the Effect
#     type.
def new_test_effect(raw_svg):
    """Returns a new Effect based on raw_svg, with all parsing done."""
    # Effect doesn't provide a provide a way to supply SVG data without using a
    # file, so use a temporary file. (We could get away with using a
    # monkey-patched sys.stdin if we didn't use Effect.affect(), but it's
    # important to use the real affect() for testing.)
    # TODO: Modify Effect to provide a way to inject SVG without using a file.
    # TODO: Reconcile Effect.affect() and parse() to simplify the
    #     svg_file/filename/stdin logic; as-is, only the svg_file path works.
    tmp_svg_path = ''
    try:
        # Write the SVG to a temp file that we can refer to by path.
        tf = tempfile.NamedTemporaryFile(
                prefix='inkscape-inkex-test-', delete=False, mode='w')
        tmp_svg_path = tf.name
        tf.write(raw_svg)
        tf.close()

        # Return an Effect that has parsed the SVG.
        e = Effect()
        e.affect(args=[tmp_svg_path], output=False)
        return e
    finally:
        os.remove(tmp_svg_path)


if __name__ == '__main__':
    # Keep sorted.
    test_support.run_unittest(GetDocumentHeightTest)
    test_support.run_unittest(GetDocumentUnitTest)
    test_support.run_unittest(GetDocumentWidthTest)
    test_support.run_unittest(UnitToUUTest)
