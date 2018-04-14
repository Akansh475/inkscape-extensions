#!/usr/bin/env python
"""
Test the svg interface for inkscape extensions.
"""

from tests.base import TestCase, test_support
from inkex.svg import etree, SVG_PARSER

def svg(svg_attrs=''):
    """Returns xml etree based on a simple SVG element.

       svg_attrs: A string containing attributes to add to the
           root <svg> element of a minimal SVG document.
    """
    return etree.fromstring(str.encode(
        '<?xml version="1.0" encoding="UTF-8" standalone="no"?>'
        '<svg {}></svg>'.format(svg_attrs)), parser=SVG_PARSER)


def uu_svg(user_unit):
    """Same as svg, but takes a user unit for the new document.

    It's based on the ratio between the SVG width and the viewBox width.
    """
    return svg('width="1{}" viewBox="0 0 1 1"'.format(user_unit))


class GetDocumentWidthTest(TestCase):
    """Tests for Effect.width."""
    def test_no_dimensions(self):
        """An empty width value should be default zero width"""
        self.assertEqual(svg().width, '0')

    def test_empty_width(self):
        """An empty width value should be the same as a missing width."""
        self.assertEqual(svg('width=""').width, '0')

    def test_empty_viewbox(self):
        """An empty viewBox value should be the same as a missing viewBox."""
        self.assertEqual(svg('viewBox=""').width, '0')

    def test_empty_width_and_viewbox(self):
        """Empty values for both should be the same as both missing."""
        self.assertEqual(svg('width="" viewBox=""').width, '0')

    def test_width_only(self):
        """Test a fixed width"""
        self.assertEqual(svg('width="120mm"').width, '120mm')

    def test_width_and_viewbox(self):
        """If both are present, width overrides viewBox."""
        self.assertEqual(svg('width="120mm" viewBox="0 0 22 99"').width, '120mm')

    def test_viewbox_only(self):
        """IF only the viewBox is present"""
        self.assertEqual(svg('viewBox="0 0 22 99"').width, 22.0)

    def test_only_valid_viewbox(self):
        """An empty width value should be the same as a missing width."""
        self.assertEqual(svg('width="" viewBox="0 0 22 99"').width, 22.0)

    def test_non_zero_viewbox_x(self):
        """Demonstrate that a non-zero x value (viewbox[0]) does not affect the width value."""
        self.assertEqual(svg('width="" viewBox="5 7 22 99"').width, 22.0)


class GetDocumentHeightTest(TestCase):
    """Tests for Effect.height."""
    def test_no_dimensions(self):
        """Test height from blank svg"""
        self.assertEqual(svg().height, '0')

    def test_empty_height(self):
        """An empty height value should be the same as a missing height."""
        self.assertEqual(svg('height=""').height, '0')

    def test_empty_viewbox(self):
        """An empty viewBox value should be the same as a missing viewBox."""
        self.assertEqual(svg('viewBox=""').height, '0')

    def test_empty_height_viewbox(self):
        """Empty values for both should be the same as both missing."""
        self.assertEqual(svg('height="" viewBox=""').height, '0')

    def test_height_only(self):
        """A simple height only in px"""
        self.assertEqual(svg('height="330px"').height, '330px')

    def test_height_and_viewbox(self):
        """If both are present, height overrides viewBox."""
        self.assertEqual(svg('height="330px" viewBox="0 0 22 99"').height, '330px')

    def test_viewbox_only(self):
        """Height from viewBox only"""
        self.assertEqual(svg('viewBox="0 0 22 99"').height, 99.0)

    def test_no_height_valid_viewbox(self):
        """An empty height value should be the same as a missing height."""
        self.assertEqual(svg('height="" viewBox="0 0 22 99"').height, 99.0)

    def test_non_zero_viewbox_y(self):
        """Demonstrate that a non-zero y value (viewbox[1]) does not affect the height value."""
        self.assertEqual(svg('height="" viewBox="5 7 22 99"').height, 99.0)


class GetDocumentUnitTest(TestCase):
    """Tests for Effect.getDocumentUnit()."""
    def test_no_dimensions(self):
        """Default units with no arguments"""
        self.assertEqual(svg().getDocumentUnit(), 'px')

    def test_width_only(self):
        """"Units from document width only"""
        # TODO: Determine whether returning 'px' in this case is the
        #     intended behavior.
        self.assertEqual(svg('width="100m"').getDocumentUnit(), 'px')

    def test_height_only(self):
        """Units from document height only"""
        # TODO: Determine whether returning 'px' in this case is the
        #     intended behavior.
        self.assertEqual(svg('height="100m"').getDocumentUnit(), 'px')

    def test_viewbox_only(self):
        """Test viewbox only document units"""
        self.assertEqual(svg('viewBox="0 0 377 565"').getDocumentUnit(), 'px')

    # Unit-ratio tests. Don't exhaustively test every unit conversion, just
    # demonstrate that the logic works.

    def test_width_and_viewbox_px(self):
        """100mm is ~377px, so unit should be 'px'."""
        self.assertEqual(svg('width="100mm" viewBox="0 0 377 565"').getDocumentUnit(), 'px')

    def test_width_and_viewbox_in(self):
        """100mm is ~3.94in, so unit should be 'in'."""
        self.assertEqual(svg('width="100mm" viewBox="0 0 3.94 5.90"').getDocumentUnit(), 'in')

    def test_unitless_width_and_viewbox(self):
        """Unitless width should be treated as 'px'."""
        # 3779px is ~1m, so unit should be 'm'.
        self.assertEqual(svg('width="3779" viewBox="0 0 1 1.5"').getDocumentUnit(), 'm')

    def test_height_with_viewbox(self):
        """150mm is ~5.90in, so unit should be 'in', but height is ignored"""
        # TODO: Determine whether returning 'px' in this case is the intended
        #     behavior.
        self.assertEqual(svg('height="150mm" viewBox="0 0 3.94 5.90"').getDocumentUnit(), 'px')

    def test_height_width_and_viewbox(self):
        """100mm is ~23.6pc, so unit should be 'pc'."""
        doc = svg('width="100mm" height="150mm" viewBox="0 0 23.6 35.4"')
        self.assertEqual(doc.getDocumentUnit(), 'pc')

    def test_large_error_reverts_to_px(self):
        """'px' instead of using the closest match 'pc'."""
        # 100mm is ~23.6pc; 24.1 is ~2% off from that, so unit should fall back
        self.assertEqual(svg('width="100mm" viewBox="0 0 24.1 35.4"').getDocumentUnit(), 'px')

    # TODO: Demonstrate that unknown width units are treated as px while
    #     determining the ratio.

    # 100px fallback tests. Although that value is an arbitrary default, it's
    # possible for users of inkex.Effect to depend on this behavior.
    # NOTE: Do not treat the existence of these tests as a reason to preserve
    # the 100px fallback logic.

    def test_bad_width_number(self):
        """Fallback test: Bad numbers default to 100"""
        # First, demonstrate that 1in is 2.54cm, so unit should be 'cm'.
        self.assertEqual(svg('width="1in" viewBox="0 0 2.54 1"').getDocumentUnit(), 'cm')

        # Corrupt the width to contain an invalid number component; note that
        # the units change to 'm'. This is because the corrupt number part is
        # replaced with 100 while the unit is preserved, producing a width of
        # "100in"; 100in is 2.54m.
        self.assertEqual(svg('width="ABCDin" viewBox="0 0 2.54 1"').getDocumentUnit(), 'm')

    def test_bad_viewbox_entry(self):
        """Fallback test: Bad viewBox default to 100"""
        # First, demonstrate that 3779px is 1m, so unit should be 'm'.
        self.assertEqual(svg('width="3779px" viewBox="0 0 1 1"').getDocumentUnit(), 'm')

        # Corrupt the viewBox to include a non-float value; note that
        # the units change to 'cm'. This is because the corrupt viewBox
        # is effectively replaced with "0 0 100 100"; 3779/100 == 37.79,
        # and 37.79px is 1cm.
        # Also note that the corruption did not touch the width element
        # of the viewBox; this fallback happens if any element is corrupt.
        self.assertEqual(svg('width="3779px" viewBox="x 0 1 1"').getDocumentUnit(), 'cm')


class UserUnitTest(TestCase):
    """Tests for methods that are based on the value of getDocumentUnit()."""

    def assertToUserUnit(self, user_unit, test_value, expected): # pylint: disable=invalid-name
        """Checks a user unit and a test_value against the expected result"""
        doc = uu_svg(user_unit)
        self.assertEqual(doc.getDocumentUnit(), user_unit, msg=svg)
        self.assertAlmostEqual(doc.unittouu(test_value), expected)

    def assertFromUserUnit(self, user_unit, value, unit, expected): # pylint: disable=invalid-name
        """Check converting from a user unity for thetest_value"""
        self.assertAlmostEqual(uu_svg(user_unit).uutounit(value, unit), expected)

    # Unit-ratio tests. Don't exhaustively test every unit conversion, just
    # demonstrate that the logic works.

    def test_unittouu_in_to_cm(self):
        """1in is ~2.54cm"""
        self.assertToUserUnit('cm', '1in', 2.54)

    def test_unittouu_yd_to_m(self):
        """1yd is ~0.9144m"""
        self.assertToUserUnit('m', '1yd', 0.9144)

    def test_unittouu_identity(self):
        """If the input and output units are the same, the input and output
           values should exactly be the same, too."""
        self.assertToUserUnit('pc', '9.87654321pc', 9.87654321)

    def test_unittouu_unitless_input(self):
        """Passing a unitless value to unittouu() should treat the units as 'px'."""
        self.assertToUserUnit('in', '96', 1) # 1in == 96px

    def test_unittouu_empty_input(self):
        """Passing an empty string to unittouu() should treat the value as zero."""
        self.assertToUserUnit('in', '', 0)

    def test_unittouu_parsing(self):
        """Test user unit parsing forms"""
        inputs = (
            '100pc',
            '100  pc',
            '   100pc',
            '100px   ',
            '+100pc',
            '100.0pc',
            '100.0e0pc',
            '10.0e1pc',
            '10.0e+1pc',
            '1000.0e-1pc',
            '.1e+3pc',
            '+.1e+3pc',
        )
        for value in inputs:
            # 100pc is ~3.937in
            self.assertToUserUnit('px', value, 1600)

    # Malformed input tests.

    def test_unittouu_bad_input_number(self):
        """Bad input number"""
        self.assertToUserUnit('cm', '1in', 2.54)
        # Demonstrate that 1in is ~2.54cm.

        # Corrupt the input to contain an invalid number component; note that
        # the result changes to zero.
        self.assertToUserUnit('cm', 'ABCDin', 0)

    def test_unittouu_bad_input_unit(self):
        """Bad input unit"""
        # Demonstrate that 1.0in passes through without change.
        self.assertToUserUnit('in', '1.0in', 1.0)

        # Corrupt the input to contain an invalid unit component; note that the
        # result changes 1/96, the ratio between inches and pixels. This is
        # because unittouu() treats unknown units as 'px'.
        self.assertToUserUnit('in', '1.0ABCD', 1/96.0)

    # Unit-ratio tests. Don't exhaustively test every unit conversion, just
    # demonstrate that the logic works.

    def test_uutounit_cm_to_in(self):
        """Convert 1 user unit ('in') to 'cm'."""
        self.assertFromUserUnit('in', 1, 'cm', 2.54) # 1in is ~2.54cm

    def test_uutounit_m_to_yd(self):
        """Convert 1 user unit ('yd') to 'm'."""
        self.assertFromUserUnit('yd', 1, 'm', 0.9144) # 1yd is ~0.9144m

    def test_uutounit_identity(self):
        """If the input and output units are the same, the input and output
           values should exactly be the same, too."""
        self.assertFromUserUnit('pc', 9.87654321, 'pc', 9.87654321)

    def test_uutounit_unknown_unit(self):
        """Demonstrate that passing an unknown unit string to uutounit()"""
        # TODO: Determine whether this is the right behavior; none of the other
        #     unit-related methods raises errors on bad units, they treat them
        #     as 'px'. It would be better for them all to be consistent, either
        #     by silently converting to 'px' here or by raising exceptions in
        #     the other methods.
        doc = uu_svg('in')
        with self.assertRaises(IOError):
            doc.uutounit(1, 'xy')

    def test_adddocumentunit_common(self):
        """Test common addDocumentUnit results"""
        # For valid float inputs, the output should be the input with the user unit appended.
        doc = uu_svg('pt')
        cases = (
            # Input, expected output
            (100, '100pt'),
            ('100', '100pt'),
            ('+100', '+100pt'),
            ('100.0', '100.0pt'),
            ('100.0e0', '100.0e0pt'),
            ('10.0e1', '10.0e1pt'),
            ('10.0e+1', '10.0e+1pt'),
            ('1000.0e-1', '1000.0e-1pt'),
            ('.1e+3', '.1e+3pt'),
            ('+.1e+3', '+.1e+3pt'),
            ('   100', '100pt'),
            ('100   ', '100pt'),
            ('  100   ', '100pt'),
        )
        for input_value, expected in cases:
            self.assertEqual(doc.addDocumentUnit(input_value), expected)

    def test_adddocumentunit_non_float(self):
        """Strings that are invalid floats should pass through unchanged."""
        doc = uu_svg('pt')
        inputs = (
            '',
            'ABCD',
            '.',
            '   ',
        )
        for value in inputs:
            self.assertEqual(doc.addDocumentUnit(value), value)


if __name__ == '__main__':
    # Keep sorted.
    test_support.run_unittest(GetDocumentHeightTest)
    test_support.run_unittest(GetDocumentUnitTest)
    test_support.run_unittest(GetDocumentWidthTest)
    test_support.run_unittest(UserUnitTest)
