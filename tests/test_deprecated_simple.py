# coding=utf-8
"""Test deprecated-simple modules"""
from __future__ import absolute_import, print_function

from pytest import approx

import inkex
import math
import os
import re


def _approx_path_coords(p):
    return [[code, approx(coords)] for (code, coords) in p]


def test_simple_imports():
    # TODO add tests for these modules
    import bezmisc
    import cspsubdiv
    import cubicsuperpath
    import ffgeom


def test_simplepath():
    import simplepath

    d = 'M12 34L56 78Z'
    p = simplepath.parsePath(d)
    assert p == [['M', [12., 34.]], ['L', [56., 78.]], ['Z', []]]

    d_out = simplepath.formatPath(p)
    d_out = d_out.replace('.0', '')
    assert d.replace(' ', '') == d_out.replace(' ', '')

    simplepath.translatePath(p, -3, -4)
    assert p == [['M', [9., 30.]], ['L', [53., 74.]], ['Z', []]]

    simplepath.scalePath(p, 10, 20)
    assert p == [['M', [90., 600.]], ['L', [530., 1480.]], ['Z', []]]

    simplepath.rotatePath(p, math.pi / 2.0, cx=5, cy=7)
    assert _approx_path_coords(p) == [['M', [-588., 92.]], ['L', [-1468., 532.]], ['Z', []]]


def test_simplestyle():
    import simplestyle

    assert simplestyle.svgcolors['blue'] == '#0000ff'
    assert simplestyle.parseStyle('foo: bar; abc-def: 123em') == {
        'foo': 'bar',
        'abc-def': '123em'
    }
    assert simplestyle.formatStyle({'foo': 'bar'}) == 'foo:bar'
    assert simplestyle.isColor('#ff0000') is True
    assert simplestyle.isColor('#f00') is True
    assert simplestyle.isColor('blue') is True
    assert simplestyle.isColor('none') is False
    assert simplestyle.isColor('nosuchcolor') is False
    assert simplestyle.parseColor('#0000ff') == (0, 0, 0xff)
    assert simplestyle.parseColor('red') == (0xff, 0, 0)
    assert simplestyle.formatColoria([0, 0x99, 0]) == '#009900'
    assert simplestyle.formatColor3i(0, 0x99, 0) == '#009900'
    assert simplestyle.formatColorfa([0, 1.0, 0]) == '#00ff00'
    assert simplestyle.formatColor3f(0, 1.0, 0) == '#00ff00'


def test_simpletransform():
    import simpletransform

    assert simpletransform.parseTransform('scale(10)') == [[10, 0, 0], [0, 10, 0]]
    assert simpletransform.parseTransform('translate(2,3)') == [[1, 0, 2], [0, 1, 3]]
    assert simpletransform.parseTransform('translate(2,3) rotate(90)') == [
        approx([0, -1, 2]), approx([1, 0, 3])
    ]
    m = simpletransform.formatTransform([[0, -1, 2], [1, 0, 3]])
    assert re.sub(r',', ' ', re.sub(r'\.0*\b', '', m)) == 'matrix(0 1 -1 0 2 3)'
    assert simpletransform.invertTransform([[1,0,2], [0,1,3]]) == [[1,0,-2],[0,1,-3]]
    assert simpletransform.composeTransform(
            [[1, 0, 2], [0, 1, 3]],
            [[0, -1, 0], [1, 0, 0]]) == [[0, -1, 2], [1, 0, 3]]

    pt = [4, 5]
    assert simpletransform.applyTransformToPoint([[0, -1, 2], [1, 0, 3]], pt) is None
    assert pt == [-3, 7]

    assert simpletransform.boxunion([3, 5, 2, 4], [4, 6, 1, 3]) == (3, 6, 1, 4)
    assert simpletransform.cubicExtrema(1, 2, 3, 4) == (1, 4)

    # TODO need cubic superpath
    assert simpletransform.applyTransformToPath
    assert simpletransform.roughBBox
    assert simpletransform.refinedBBox

    # TODO need node
    assert simpletransform.fuseTransform
    assert simpletransform.composeParents
    assert simpletransform.applyTransformToNode
    assert simpletransform.computeBBox
    assert simpletransform.computePointInNode


def test_namespace_pollution():
    # modules with legacy proxies

    import optparse
    assert optparse.OptionParser == inkex.optparse.OptionParser

    import lxml.etree
    assert lxml.etree.Element == inkex.etree.Element

    # skip:
    # - copy
    # - os
    # - random
    # - re
    # - sys
    # - math.*


def test_inkex_namespace():
    from inkex import InkOption
    assert 'inkbool' in InkOption.TYPES
    assert 'inkbool' in InkOption.TYPE_CHECKER

    from inkex import NSS
    assert NSS['svg'] == 'http://www.w3.org/2000/svg'

    from inkex import addNS
    assert addNS('rect', 'svg') == '{http://www.w3.org/2000/svg}rect'

    from inkex import are_near_relative
    assert are_near_relative(123.4, 123.5, 1e-3)
    assert not are_near_relative(123.4, 123.5, 1e-4)

    # skip:
    # - from inkex import check_inkbool (InkOption implementation detail)

    from inkex import debug
    from inkex import errormsg
    from inkex import localize


def test_inkex_Effect():
    from inkex import Effect

    args = [
        '--id', 'curve',
        os.path.join(os.path.dirname(__file__), 'data', 'ref_curves.svg'),
    ]

    e = Effect()
    e.affect(args)

    # assigned in __init__
    assert e.document.getroot() is not None
    assert isinstance(e.selected, dict)
    assert list(e.selected) == ['curve']
    assert isinstance(e.doc_ids, dict)
    assert isinstance(e.options.ids, list)
    assert e.args == args[-1:]
    assert e.OptionParser.add_option is not None

    # methods
    assert e.getselected() is None
    assert e.getdocids() is None
    node = e.getElementById('arc')
    assert node.tag == '{http://www.w3.org/2000/svg}path'
    assert node.get('id') == 'arc'
    assert e.getParentNode(node).tag == '{http://www.w3.org/2000/svg}g'
    assert e.getNamedView().tag == \
            '{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}namedview'
    assert e.createGuide(10, 20, 45).tag == \
            '{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}guide'
    assert e.uniqueId('foo').startswith('foo')
    assert e.xpathSingle('//svg:path').tag == '{http://www.w3.org/2000/svg}path'
    assert e.getDocumentWidth() == '1000'
    assert e.getDocumentHeight() == '1000'
    assert e.getDocumentUnit() == 'px'
    assert e.unittouu('1in') == 96
    assert e.uutounit(192, 'in') == 2
    assert e.addDocumentUnit('3') == '3px'

    # skip:
    # - e.ctx
    # - e.getposinlayer
    # - e.original_document
