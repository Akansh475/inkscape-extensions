#!/usr/bin/env python
# coding=utf-8
"""
Test elements extra logic from svg xml lxml custom classes.
"""

from lxml import etree

import inkex

from inkex.elements import (
    ShapeElement, Group, Pattern, Guide, Polyline, Use, Defs,
    TextElement, TextPath, Tspan, FlowPara, FlowRoot, FlowRegion, FlowSpan,
    PathElement, Rectangle, Circle, Ellipse, Anchor, Line as LineElement
)
from inkex.paths import Move, Line
from inkex.utils import FragmentError, PY3
from inkex.transforms import Transform
from inkex.styles import Style
from inkex.tester import TestCase
from inkex.tester.svg import svg_file

class FakeShape(ShapeElement):
    tag_name = 'fake'

class ElementTestCase(TestCase):
    """Base element test case"""
    source_file = 'complextransform.test.svg'
    tag = 'svg'

    def setUp(self):
        super(ElementTestCase, self).setUp()
        self.svg = svg_file(self.data_file('svg', self.source_file))
        self.elem = self.svg.getElement('//svg:{}'.format(self.tag))

    def test_print(self):
        """Print element as string"""
        self.assertEqual(str(self.elem), self.tag)

    def assertElement(self, elem, compare):
        """Assert an element"""
        if PY3:
            self.assertEqual(elem.tostring(), compare)

class CoreElementTestCase(ElementTestCase):
    """Test core element functionality"""
    tag = 'g'

    def test_reference_count(self):
        """
        Test inkex.element.BaseElement-derived object type is preserved on adding to group

        See https://gitlab.com/inkscape/extensions/issues/81 for details
        """
        grp = Group()
        for _ in range(10):
            rect = Rectangle()
            grp.add(rect)

        for elem in grp:
            self.assertEqual(type(elem), Rectangle)

    def test_abstract_raises(self):
        """Abstract classes cannot be instantiated"""
        self.assertRaises(AssertionError, ShapeElement)
        self.assertRaises(NotImplementedError, FakeShape().get_path)
        self.assertRaises(AttributeError, FakeShape().set_path, None)

    def test_findall(self):
        """Findall elements in svg"""
        groups = self.svg.findall('svg:g')
        self.assertEqual(len(groups), 1)

    def test_add(self):
        """Can add single or multiple elements with passthrough"""
        elem = self.svg.getElementById('D')
        group = elem.add(Group(id='foo'))
        self.assertEqual(group.get('id'), 'foo')
        groups = elem.add(Group(id='f1'), Group(id='f2'))
        self.assertEqual(len(groups), 2)
        self.assertEqual(groups[0].get('id'), 'f1')
        self.assertEqual(groups[1].get('id'), 'f2')

    def test_creation(self):
        """Create elements with attributes"""
        group = Group().update(inkscape__label='Foo')
        self.assertEqual(group.get('inkscape:label'), 'Foo')
        group = Group().update(inkscape__label='Bar')
        self.assertEqual(group.label, 'Bar')

    def test_chained_multiple_attrs(self):
        """Set multiple attributes at a time"""
        group = Group().update(
            attr1='A',
            attr2='B'
        ).update(
            attr3='C',
            attr4='D'
        )
        self.assertEqual(group.get('attr1'), 'A')
        self.assertEqual(group.get('attr2'), 'B')
        self.assertEqual(group.get('attr3'), 'C')
        self.assertEqual(group.get('attr4'), 'D')

        # remove attributes, setting them to None
        group.update(
            attr1=None,
            attr4=None
        )

        self.assertEqual(group.get('attr1'), None)
        self.assertEqual(group.get('attr2'), 'B')
        self.assertEqual(group.get('attr3'), 'C')
        self.assertEqual(group.get('attr4'), None)

        self.assertEqual(group.pop('attr2'), 'B')
        self.assertEqual(group.pop('attr3'), 'C')

    def test_tostring(self):
        """Elements can be printed as strings"""
        self.assertEqual(Group().tostring(), b'<g/>')
        elem = Group(id='bar')
        path = elem.add(Tspan(id='foo'))
        elem.transform.add_translate(50, 50)
        path.style['fill'] = 'red'
        self.assertEqual(elem.tostring(),
            b'<g transform="translate(50, 50)"><tspan id="foo" style="fill:red"/></g>')

    def test_set_wrapped_attribute(self):
        """Remove wrapped attribute using .set()"""
        group = Group().update(
            transform=Transform(scale=2)
        )
        self.assertEqual(group.transform.matrix[0][0], 2)
        self.assertEqual(group.transform.matrix[1][1], 2)

        group.update(
            transform=None
        )
        self.assertEqual(group.transform, Transform())

    def test_pop_wrapped_attribute(self):
        """Remove wrapped attribute using .pop()"""
        group = Group()

        self.assertEqual(group.pop('transform'), Transform())

        group.update(
            transform=Transform(scale=2)
        )
        self.assertEqual(group.pop('transform'), Transform(scale=2))
        self.assertEqual(group.pop('transform'), Transform())
        self.assertRaises(AttributeError, getattr, group, 'foo')

    def test_pop_regular_attribute(self):
        """Remove wrapped attribute using .pop()"""
        group = Group()

        self.assertEqual(group.get('attr1'), None)

        group.update(
            attr1="42"
        )
        self.assertEqual(group.pop('attr1'), "42")
        self.assertEqual(group.pop('attr1'), None)

    def test_sort_selected(self):
        """Are the selected items sorted"""
        self.svg.set_selected('G', 'B', 'D', 'F')
        self.assertEqual(tuple(self.svg.selected), ('G', 'B', 'D', 'F'))
        items = self.svg.get_z_selected()
        self.assertTrue(isinstance(items, dict))
        self.assertEqual(tuple(items), ('B', 'D', 'F', 'G'))

        self.svg.set_selected()
        self.assertEqual(tuple(self.svg.get_z_selected()), ())
        a_to_g = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
        self.svg.set_selected(*a_to_g)
        self.assertEqual(tuple(self.svg.get_z_selected()), a_to_g)
        self.svg.set_selected('X', 'Y', 'Z', 'A')
        self.assertEqual(tuple(self.svg.get_z_selected()), ('A',))

    def test_transform(self):
        """In-place modified transforms are retained"""
        elem = self.svg.getElementById('D')
        self.assertEqual(str(elem.transform), 'translate(30, 10)')
        elem.transform.add_translate(-10, 10)
        self.assertEqual(str(elem.transform), 'translate(20, 20)')

    def test_scale(self):
        """In-place scaling from blank transform"""
        elem = self.svg.getElementById('F')
        self.assertEqual(elem.transform, Transform())
        self.assertEqual(elem.get('transform'), None)
        elem.transform.add_scale(1.0666666666666667, 1.0666666666666667)
        self.assertEqual(elem.get('transform'), Transform(scale=1.06667))
        self.assertIn(b'transform', etree.tostring(elem))

    def test_in_place_transforms(self):
        """Do style and transforms update correctly"""
        elem = self.svg.getElementById('D')
        self.assertEqual(type(elem.transform), Transform)
        self.assertEqual(type(elem.style), Style)
        self.assertTrue(elem.transform)
        elem.transform = Transform()
        self.assertEqual(elem.transform, Transform())
        self.assertEqual(elem.get('transform'), None)
        self.assertNotIn(b'transform', etree.tostring(elem))
        elem.transform.add_translate(10, 10)
        self.assertIn(b'transform', etree.tostring(elem))
        elem.transform.add_translate(-10, -10)
        self.assertNotIn(b'transform', etree.tostring(elem))

    def test_update_consistant(self):
        """Update doesn't keep callbacks around"""
        elem = self.svg.getElementById('D')
        tr_a = Transform(translate=(10, 10))
        tr_b = Transform(translate=(-20, 15))
        elem.transform = tr_a
        elem.transform = tr_b
        self.assertEqual(str(elem.transform), 'translate(-20, 15)')
        tr_a.add_translate(10, 10)
        self.assertEqual(str(elem.transform), 'translate(-20, 15)')
        elem.set('transform', None)
        self.assertEqual(elem.get('transform'), None)

    def test_in_place_style(self):
        """Do styles update when we set them"""
        elem = self.svg.getElementById('D')
        elem.style['fill'] = 'purpleberry'
        self.assertEqual(elem.get('style'), 'fill:purpleberry')
        elem.style = {'marker': 'flag'}
        self.assertEqual(elem.get('style'), 'marker:flag')
        elem.style = Style(stroke='gammon')
        self.assertEqual(elem.get('style'), 'stroke:gammon')
        elem.style.update('grape:2;strawberry:nice;')
        self.assertEqual(elem.get('style'), 'stroke:gammon;grape:2;strawberry:nice')

    def test_random_id(self):
        """Test setting a random id"""
        elem = self.svg.getElementById('D')
        elem.set_random_id('Thing')
        self.assertEqual(elem.get('id'), 'Thing5815')
        elem.set_random_id('Thing', size=2)
        self.assertEqual(elem.get('id'), 'Thing85')
        elem.set_random_id()
        self.assertEqual(elem.get('id'), 'path5392')

    def test_random_ids(self):
        """Test setting a tree of ids"""
        elem = self.svg.getElementById('D')
        self.svg.set_random_ids(prefix='TreeItem')
        self.assertEqual(self.svg.get('id'), 'TreeItem5815')
        self.assertEqual(self.svg[0].get('id'), 'TreeItem8555')
        self.assertEqual(elem.get('id'), 'TreeItem2036')

    def test_set_id_backlinks(self):
        """Changing an id can update backlinks"""
        elem = self.svg.getElementById('path1')
        elem.set_id('plant54', True)
        self.assertEqual(self.svg.getElementById('G').get('xlink:href'), '#plant54')
        self.assertEqual(self.svg.getElementById('G').href, elem)
        self.assertEqual(str(self.svg.getElementById('B').style), 'fill:#eee;joker:url(#plant54)')

    def test_bounding_box(self):
        """Elements can have bounding boxes"""
        elem = self.svg.getElementById('D')
        self.assertEqual(tuple(elem.bounding_box()), ((60.0, 100.0), (130.0, 170.00)))
        self.assertTrue(elem.bounding_box().center.is_close((80.0, 150.0)))
        self.assertEqual(tuple(TextElement(x='10', y='5').bounding_box()), ((10, 10), (5, 5)))
        group = Group(elem)
        self.assertEqual(elem.bounding_box(), group.bounding_box())

    def test_replace_with(self):
        """Replacing nodes in a tree"""
        rect = self.svg.getElementById('E')
        path = rect.to_path_element()
        rect.replace_with(path)
        self.assertEqual(rect.getparent(), None)
        self.assertEqual(path.getparent(), self.svg.getElementById('C'))

    def test_path(self):
        """Test getting paths"""
        self.assertFalse(TextPath().get_path())
        self.assertFalse(TextElement().get_path())
        self.assertFalse(FlowRegion().get_path())
        self.assertFalse(FlowRoot().get_path())
        self.assertFalse(FlowPara().get_path())
        self.assertFalse(FlowSpan().get_path())
        self.assertFalse(Tspan().get_path())

    def test_descendants(self):
        """Elements can walk their descendants"""
        ids = tuple(elem.get('id') for elem in self.svg.descendants())
        self.assertEqual(ids, (
            None, None, 'path1', None,
            'base', 'metadata7',
            None, None, None, None, None,
            'A', 'B', 'C', 'D', 'E', 'F', 'G',
            'H', 'I', 'J',
        ))

class LineElementTestCase(ElementTestCase):
    """Test LineElements"""
    def test_new_line(self):
        line = LineElement.new((10, 10), (20, 20))
        self.assertElement(line, b'<line x1="10" y1="10" x2="20" y2="20"/>')

class PathElementTestCase(ElementTestCase):
    """Test PathElements"""
    source_file = 'with-lpe.svg'
    tag = 'path'

    def test_new_path(self):
        """Test new path element"""
        path = PathElement.new(path=[Move(10,10), Line(20, 20)])
        self.assertEqual(path.get('d'), 'M 10 10 L 20 20')

    def test_original_path(self):
        """LPE paths can return their original paths"""
        lpe = self.svg.getElementById('lpe')
        nolpe = self.svg.getElementById('nolpe')
        self.assertEqual(str(lpe.path), 'M 30 30 L -10 -10 Z')
        self.assertEqual(str(lpe.original_path), 'M 20 20 L 10 10 Z')
        self.assertEqual(str(nolpe.path), 'M 30 30 L -10 -10 Z')
        self.assertEqual(str(nolpe.original_path), 'M 30 30 L -10 -10 Z')

        lpe.original_path = "M 60 60 L 5 5"
        self.assertEqual(lpe.get('inkscape:original-d'), 'M 60 60 L 5 5')
        self.assertEqual(lpe.get('d'), 'M 30 30 L -10 -10 Z')

        lpe.path = "M 60 60 L 15 15 Z"
        self.assertEqual(lpe.get('d'), 'M 60 60 L 15 15 Z')

        nolpe.original_path = "M 60 60 L 5 5"
        self.assertEqual(nolpe.get('inkscape:original-d', None), None)
        self.assertEqual(nolpe.get('d'), 'M 60 60 L 5 5')

class PolylineElementTestCase(ElementTestCase):
    """Test the polyline elements support"""
    tag = 'polyline'

    def test_type(self):
        """Polyline have their own types"""
        self.assertTrue(isinstance(self.elem, inkex.elements.Polyline))

    def test_polyline_points(self):
        """Basic tests for points attribute as a path"""
        pol = Polyline(points='10,10 50,50 10,15 15,10')
        self.assertEqual(str(pol.path), 'M 10 10 L 50 50 L 10 15 L 15 10')
        pol.path = "M 10 10 L 30 9 L 1 2 C 10 45 3 4 45 60 M 35 35"
        self.assertEqual(pol.get('points'), '10,10 30,9 1,2 45,60 35,35')

class PolygonElementTestCase(ElementTestCase):
    """Test Polygon Elements"""
    tag = 'polygon'

    def test_type(self):
        """Polygons have their own types"""
        self.assertTrue(isinstance(self.elem, inkex.elements.Polygon))

    def test_conversion(self):
        """Polygones are converted to paths"""
        pol = inkex.elements.Polygon(points='10,10 50,50 10,15 15,10')
        self.assertEqual(str(pol.path), 'M 10 10 L 50 50 L 10 15 L 15 10 Z')

class LineElementTestCase(ElementTestCase):
    """Test Line Elements"""
    tag = 'line'

    def test_type(self):
        """Lines have their own types"""
        self.assertTrue(isinstance(self.elem, inkex.elements.Line))

    def test_conversion(self):
        """Lines are converted to paths"""
        pol = inkex.elements.Line(x1='2', y1='3', x2='4', y2='5')
        self.assertEqual(str(pol.path), 'M 2 3 L 4 5')

class PatternTestCase(ElementTestCase):
    """Test Pattern elements"""
    tag = 'pattern'

    def test_pattern_transform(self):
        """Patterns have a transformation of their own"""
        pattern = Pattern()
        self.assertEqual(pattern.patternTransform, Transform())
        pattern.patternTransform.add_translate(10, 10)
        self.assertEqual(pattern.get('patternTransform'), 'translate(10, 10)')

class GroupTest(ElementTestCase):
    """Test extra functionality on a group element"""
    tag = 'g'

    def test_new_group(self):
        """Test creating groups"""
        svg = Group.new('layerA', True, Group.new('groupA', False, Rectangle()))
        self.assertElement(svg,\
            b'<g inkscape:label="layerA" inkscape:groupmode="layer">'\
            b'<g inkscape:label="groupA"><rect/></g></g>')

    def test_transform_property(self):
        """Test getting and setting a transform"""
        self.assertEqual(str(self.elem.transform), 'matrix(1.44985 0 0 1.36417 -107.03 -167.362)')
        self.elem.transform = 'translate(12, 14)'
        self.assertEqual(self.elem.transform, Transform('translate(12, 14)'))
        self.assertEqual(str(self.elem.transform), 'translate(12, 14)')

    def test_groupmode(self):
        """Get groupmode is layer"""
        self.assertEqual(self.svg.getElementById('A').groupmode, 'layer')
        self.assertEqual(self.svg.getElementById('C').groupmode, 'group')

    def test_get_path(self):
        """Group path is combined children"""
        self.assertEqual(
            str(self.svg.getElementById('A').get_path()),
            'M -108.539 517.61 L -87.6093 496.117 L -98.3066 492.768 L -69.9352 492.301 L -55.5172'
            ' 506.163 L -66.2145 502.814 L -87.1445 524.307 M 60.0914 498.693 L 156.784 439.145 L'
            ' 240.218 491.183 L 143.526 550.731 z M -176.909 458.816 a 64.2385 38.9175 -7.86455 1'
            ' 0 88.3701 -19.0784 a 64.2385 38.9175 -7.86455 0 0 -88.3701 19.0784 z M -300.162'
            ' 513.715 L -282.488 509.9 Z M -214.583 540.504 L -209.001 448.77 M -193.189 547.201 L'
            ' -238.536 486.266 L -185.049 503.008 L -230.396 442.073 M -193.189 547.201 L -238.536'
            ' 486.266 L -185.049 503.008 L -230.396 442.073 Z')


class RectTest(ElementTestCase):
    """Test extra functionality on a rectangle element"""
    tag = 'rect'

    def test_compose_transform(self):
        """Composed transformation"""
        self.assertEqual(self.elem.transform, Transform('rotate(16.097889)'))
        self.assertEqual(str(self.elem.composed_transform()),
                         'matrix(0.754465 -0.863362 1.13818 1.31905 -461.593 215.192)')

    def test_effetive_stylesheet(self):
        """Test the non-parent combination of styles"""
        self.assertEqual(str(self.elem.effective_style()),\
            'fill:#0000ff;stroke-width:1px')
        self.assertEqual(str(self.elem.getparent().effective_style()),\
            'fill:#0000ff;stroke-width:1px;stroke:#f00')

    def test_compose_stylesheet(self):
        """Test finding the composed stylesheet for the shape"""
        self.assertEqual(str(self.elem.style), 'fill:#0000ff;stroke-width:1px')
        self.assertEqual(str(self.elem.composed_style()),
                         'fill:#0000ff;stroke:#d88;joker:url(#path1);stroke-width:1px')

    def test_path(self):
        """Rectangle path"""
        self.assertEqual(self.elem.get_path(), 'M 200.0,200.0 h100.0v100.0h-100.0 z')
        self.assertEqual(str(self.elem.path), 'M 200 200 h 100 v 100 h -100 z')

class PathTest(ElementTestCase):
    """Test path extra functionality"""
    tag = 'path'

    def test_apply_transform(self):
        """Transformation can be applied to path"""
        path = self.svg.getElementById('D')
        path.transform = Transform(translate=(10, 10))
        self.assertEqual(path.get('d'), 'M30,130 L60,130 L60,120 L70,140 L60,160 L60,150 L30,150')
        path.apply_transform()
        self.assertEqual(path.get('d'), 'M 30 130 L 60 130 L 60 120 '
                                        'L 70 140 L 60 160 L 60 150 L 30 150')
        self.assertFalse(path.transform)

class CircleTest(ElementTestCase):
    """Test extra functionality on a circle element"""
    tag = 'circle'

    def test_new(self):
        """Test new circles"""
        elem = Circle.new(10, 10, 50)
        self.assertElement(elem, b'<circle cx="10" cy="10" r="50"/>')
        elem = Ellipse.new(10, 10, 15, 10)
        self.assertElement(elem, b'<ellipse cx="10" cy="10" rx="15" ry="10"/>')

    def test_path(self):
        """Circle path"""
        self.assertEqual(self.elem.get_path(),
                         'M 100.0,50.0 a 50.0,50.0 0 1 0 50.0, '
                         '50.0 a 50.0,50.0 0 0 0 -50.0, -50.0 z')

class AnchorTest(ElementTestCase):
    def test_new(self):
        link = Anchor.new('https://inkscape.org', Rectangle())
        self.assertElement(link, b'<a xlink:href="https://inkscape.org"><rect/></a>')

class NamedViewTest(ElementTestCase):
    """Test the sodipodi namedview tag"""
    def test_guides(self):
        """Create a guide and see a list of them"""
        self.svg.namedview.add(Guide().move_to(0, 0, 0))
        self.svg.namedview.add(Guide().move_to(0, 0, '90'))
        self.assertEqual(len(self.svg.namedview.get_guides()), 2)

class TextTest(ElementTestCase):
    """Test all text functions"""
    def test_append_superscript(self):
        """Test adding superscript"""
        tap = TextPath()
        tap.append(Tspan.superscript('th'))
        self.assertEqual(len(tap), 1)

class UseTest(ElementTestCase):
    """Test extra functionality on a use element"""
    tag = 'use'

    def test_path(self):
        """Use path follows ref"""
        self.assertEqual(str(self.elem.path), 'M 0 0 L 10 10 Z')

    def test_empty_ref(self):
        """An empty ref or None ref doesn't cause an error"""
        use = Use()
        use.set('xlink:href', 'something')
        self.assertRaises(FragmentError, getattr, use, 'href')
        elem = self.svg.add(Use())
        self.assertEqual(elem.href, None)
        elem.set('xlink:href', '')
        self.assertEqual(elem.href, None)
        elem.set('xlink:href', '#badref')
        self.assertEqual(elem.href, None)
        elem.set('xlink:href', self.elem.get('xlink:href'))
        self.assertEqual(elem.href.get('id'), 'path1')

    def test_unlink(self):
        """Test use tag unlinking"""
        elem = self.elem.unlink()
        self.assertEqual(str(elem.path), 'M 0 0 L 10 10 Z')
        self.assertEqual(elem.tag_name, 'path')
        self.assertEqual(elem.getparent().get('id'), 'C')

class SymbolTest(ElementTestCase):
    """Test Symbol elements"""
    source_file = 'symbol.svg'
    tag = 'symbol'

    def test_unlink_symbol(self):
        """Test unlink symbols"""
        use = self.svg.getElementById('plane01')
        self.assertEqual(use.tag_name, 'use')
        self.assertEqual(use.href.tag_name, 'symbol')
        # Unlinking should replace symbol with group
        elem = use.unlink()
        self.assertEqual(elem.tag_name, 'g')
        self.assertEqual(str(elem.transform), 'translate(18, 16)')
        self.assertEqual(elem[0].tag_name, 'title')
        self.assertEqual(elem[1].tag_name, 'rect')

class DefsTest(ElementTestCase):
    """Test the definitions tag"""
    source_file = 'shapes.svg'
    tag = 'defs'

    def test_defs(self):
        """Make sure defs can be seen in the nodes of an svg"""
        self.assertTrue(isinstance(self.svg.defs, Defs))
        defs = self.svg.getElementById('defs33')
        self.assertTrue(isinstance(defs, Defs))

class StyleTest(ElementTestCase):
    """Test a style tag"""
    source_file = 'css.svg'
    tag = 'style'

    def test_style(self):
        """Make sure style tags can be loaded and saved"""
        css = self.svg.stylesheet
        self.assertTrue(css)
