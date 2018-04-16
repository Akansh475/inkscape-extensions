# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 - Martin Owens <doctormo@mgail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
"""
Provide some documentation to existing extensions about why they're failing.
"""
#
# We ignore a lot of pylint warnings here:
#
# pylint: disable=invalid-name,unused-argument,missing-docstring,too-many-public-methods
#

import sys
from argparse import ArgumentParser

import inkex

from inkex.localize import _


class DeprecatedEffect(object):
    """An Inkscape effect, takes SVG in and outputs SVG"""
    def __init__(self):
        super(DeprecatedEffect, self).__init__()
        # These are things we reference in the deprecated code, they are provided
        # by the new effects code, but we want to keep this as a Mixin so these
        # items will keep pylint happy and let use check our code as we write.
        if not hasattr(self, 'svg'):
            self.svg = inkex.svg.SvgDocumentElement()
        if not hasattr(self, 'arg_parser'):
            self.arg_parser = ArgumentParser()
        if not hasattr(self, 'run'):
            self.run = self.affect

    warned_about = set()
    def warn_about(self, name, msg=_('{} is deprecated and should be removed')):
        """Give the user a warning about their extension using a deprecated API"""
        inkex.localize.localize()
        if name not in self.warned_about:
            sys.stderr.write(msg.format('Effect.' + name) + '\n')
            self.warned_about.add(name)

    @property
    def OptionParser(self):
        self.warn_about('OptionParser', _('{} or `optparse` is very old, it was '\
            'deprecated when python 2.7 came out in 2009 and is now replaced with '
            '`argparser`. You must change `self.OptionParser.add_option` to '
            '`self.arg_parser.add_argument` the arguments are similar.'))
        return self

    def add_option(self, *args, **kw):
        # Convert type string into type method as needed
        kw['type'] = {
            'string': str,
        }.get(kw.get('type', 'string'))
        self.arg_parser.add_argument(*args, **kw)

    def effect(self):
        self.warn_about('effect', _('{} method is now a required method. It should '\
            'be created in your extension class, even if it does nothing.'))

    @property
    def current_layer(self):
        self.warn_about('current_layer', _('{} is now a method in the svg '\
            'document. Use `self.svg.get_current_layer()` instead.'))
        return self.svg.get_current_layer()

    @property
    def view_center(self):
        self.warn_about('view_center', _('{} is now a method in the svg '\
            'document. Use `self.svg.get_center_position()` instead.'))
        return self.svg.get_center_position()

    @property
    def selected(self):
        self.warn_about('selected', _('{} is now a dictionary in the svg '\
            'document. Use self.svg.selected instead.'))
        return self.svg.selected

    @property
    def doc_ids(self):
        self.warn_about('doc_ids', _('{} is now a method in the svg '\
            'document. Use `self.svg.get_ids()` instead.'))
        return self.svg.get_ids()

    def getElementById(self, eid):
        self.warn_about('getElementById', _('{} is now a method in the svg '\
            'document. Use `self.svg.getElementById(eid)` instead.'))
        return self.svg.getElementById(eid)

    def xpathSingle(self, xpath):
        self.warn_about('xpathSingle', _('{} is now a new method in the svg '\
            'document. Use `self.svg.getElement(path)` instead.`'))
        return self.svg.getElement(xpath)

    def getParentNode(self, node):
        self.warn_about('getParentNode', _('{} should never have existed. '\
            'lxml always had a getparent() method and that should be used '
            'instead of this custom Effect method.'))
        return node.getparent()

    def getNamedView(self):
        self.warn_about('getNamedView', _('{} is now a property of the svg '\
            'document. Use `self.svg.namedview` to access this element'))
        return self.svg.namedview

    def createGuide(self, posX, posY, angle):
        self.warn_about('createGuide', _('{} is now a method of the namedview '\
            'element object. Use `self.svg.namedview.create_guide(x, y, a)` instead'))
        return self.svg.namedview.create_guide(posX, posY, angle)

    def affect(self, args=sys.argv[1:], output=True):
        self.warn_about('affect', _('{} is now `Effect.run()` with the same args'))
        return self.run(args=args, output=output)

    def uniqueId(self, old_id, make_new_id=True):
        self.warn_about('uniqueId', _('{} is now a method in the svg document. '\
            ' Use `self.svg.get_unique_id(old_id)` instead.'))
        return self.svg.get_unique_id(old_id)

    @property
    def __uuconv(self):
        self.warn_about('__uuconv', _('{} wasn\'t even a public property, '\
            'why is your effect extension even using it? Shoudl be '
            'inkex.units.CONVERSIONS'))
        return inkex.units.CONVERSIONS

    def getDocumentWidth(self):
        self.warn_about('getDocumentWidth', _('{} is now a property of the svg '\
            'document. Use `self.svg.width` instead.'))
        return self.svg.width

    def getDocumentHeight(self):
        self.warn_about('getDocumentHeight', _('{} is now a property of the svg '\
            'document. Use `self.svg.height` instead.'))
        return self.svg.height

    def getDocumentUnit(self):
        self.warn_about('getDocumentUnit', _('{} is now a property of the svg '\
            'document. Use `self.svg.unit` instead.'))
        return self.svg.unit

    def unittouu(self, string):
        self.warn_about('unittouu', _('{} is now a method in the svg '\
            'document. Use `self.svg.unittouu(str)` instead.'))
        return self.svg.unittouu(string)

    def uutounit(self, val, unit):
        self.warn_about('uutounit', _('{} is now a method in the svg '\
            'document. Use `self.svg.uutounit(value, unit)` instead.'))
        return self.svg.uutounit(val, unit)

    def addDocumentUnit(self, value):
        self.warn_about('addDocumentUnit', _('{} is now a method in the svg '\
            'document. Use `self.svg.add_unit(value)` instead.'))
        return self.svg.add_unit(value)

# vim: expandtab shiftwidth=4 tabstop=8 softtabstop=4 fileencoding=utf-8 textwidth=99
