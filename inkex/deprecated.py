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

import os
import sys
import warnings

from argparse import ArgumentParser

import inkex
import inkex.utils

from inkex.localize import _

warnings.simplefilter("default")
# To load each of the deprecated sub-modules (the ones without a namespace)
# we will add the directory to our pythonpath so older scripts can find them

INKEX_DIR = os.path.abspath(os.path.dirname(__file__))
SIMPLE_DIR = os.path.join(INKEX_DIR, 'deprecated-simple')

if os.path.isdir(SIMPLE_DIR):
    sys.path.append(SIMPLE_DIR)

class DeprecatedEffect(object):
    """An Inkscape effect, takes SVG in and outputs SVG, providing a deprecated layer"""
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

    @staticmethod
    def _depricated(name, msg=_('{} is deprecated and should be removed')):
        """Give the user a warning about their extension using a deprecated API"""
        msg = msg.format('Effect.' + name)
        warnings.warn(msg, DeprecationWarning, stacklevel=3)

    @property
    def OptionParser(self):
        self._depricated('OptionParser', _('{} or `optparse` is very old, it was '\
            'deprecated when python 2.7 came out in 2009 and is now replaced with '
            '`argparser`. You must change `self.OptionParser.add_option` to '
            '`self.arg_parser.add_argument` the arguments are similar.'))
        return self

    def add_option(self, *args, **kw):
        # Convert type string into type method as needed
        if 'type' in kw:
            kw['type'] = {
                'string': str,
                'int': int,
                'float': float,
                'inkbool': inkex.utils.inkbool,
            }.get(kw['type'])
        if kw.get('action', None) == 'store':
            # Default store action not required, removed.
            kw.pop('action')
        self.arg_parser.add_argument(*args, **kw)

    def effect(self):
        self._depricated('effect', _('{} method is now a required method. It should '\
            'be created in your extension class, even if it does nothing.'))

    @property
    def current_layer(self):
        self._depricated('current_layer', _('{} is now a method in the svg '\
            'document. Use `self.svg.get_current_layer()` instead.'))
        return self.svg.get_current_layer()

    @property
    def view_center(self):
        self._depricated('view_center', _('{} is now a method in the svg '\
            'document. Use `self.svg.get_center_position()` instead.'))
        return self.svg.get_center_position()

    @property
    def selected(self):
        self._depricated('selected', _('{} is now a dictionary in the svg '\
            'document. Use self.svg.selected instead.'))
        return self.svg.selected

    @property
    def doc_ids(self):
        self._depricated('doc_ids', _('{} is now a method in the svg '\
            'document. Use `self.svg.get_ids()` instead.'))
        return self.svg.get_ids()

    def getElementById(self, eid):
        self._depricated('getElementById', _('{} is now a method in the svg '\
            'document. Use `self.svg.getElementById(eid)` instead.'))
        return self.svg.getElementById(eid)

    def xpathSingle(self, xpath):
        self._depricated('xpathSingle', _('{} is now a new method in the svg '\
            'document. Use `self.svg.getElement(path)` instead.`'))
        return self.svg.getElement(xpath)

    def getParentNode(self, node):
        self._depricated('getParentNode', _('{} should never have existed. '\
            'lxml always had a getparent() method and that should be used '
            'instead of this custom Effect method.'))
        return node.getparent()

    def getNamedView(self):
        self._depricated('getNamedView', _('{} is now a property of the svg '\
            'document. Use `self.svg.namedview` to access this element'))
        return self.svg.namedview

    def createGuide(self, posX, posY, angle):
        self._depricated('createGuide', _('{} is now a method of the namedview '\
            'element object. Use `self.svg.namedview.create_guide(x, y, a)` instead'))
        return self.svg.namedview.create_guide(posX, posY, angle)

    def affect(self, args=sys.argv[1:]): # pylint: disable=dangerous-default-value
        # We need a list as the default value to preserve backwards compatibility
        self._depricated('affect', _('{} is now `Effect.run()` with the same args'))
        return self.run(args=args)

    def uniqueId(self, old_id, make_new_id=True):
        self._depricated('uniqueId', _('{} is now a method in the svg document. '\
            ' Use `self.svg.get_unique_id(old_id)` instead.'))
        return self.svg.get_unique_id(old_id)

    @property
    def __uuconv(self):
        self._depricated('__uuconv', _('{} wasn\'t even a public property, '\
            'why is your effect extension even using it? Should be '
            'inkex.units.CONVERSIONS'))
        return inkex.units.CONVERSIONS

    def getDocumentWidth(self):
        self._depricated('getDocumentWidth', _('{} is now a property of the svg '\
            'document. Use `self.svg.width` instead.'))
        return self.svg.width

    def getDocumentHeight(self):
        self._depricated('getDocumentHeight', _('{} is now a property of the svg '\
            'document. Use `self.svg.height` instead.'))
        return self.svg.height

    def getDocumentUnit(self):
        self._depricated('getDocumentUnit', _('{} is now a property of the svg '\
            'document. Use `self.svg.unit` instead.'))
        return self.svg.unit

    def unittouu(self, string):
        self._depricated('unittouu', _('{} is now a method in the svg '\
            'document. Use `self.svg.unittouu(str)` instead.'))
        return self.svg.unittouu(string)

    def uutounit(self, val, unit):
        self._depricated('uutounit', _('{} is now a method in the svg '\
            'document. Use `self.svg.uutounit(value, unit)` instead.'))
        return self.svg.uutounit(val, unit)

    def addDocumentUnit(self, value):
        self._depricated('addDocumentUnit', _('{} is now a method in the svg '\
            'document. Use `self.svg.add_unit(value)` instead.'))
        return self.svg.add_unit(value)


def deprecate(func):
    """Function decorator for deprecation functions which have a one-liner
    equivalent in the new API. The one-liner has to passed as a string
    to the decorator.

    >>> @deprecate
    >>> def someOldFunction(*args):
    >>>     '''Example replacement code someNewFunction('foo', ...)'''
    >>>     someNewFunction('foo', *args)

    Or if the args API is the same:

    >>> someOldFunction = deprecate(someNewFunction)

    """
    def _inner(*args, **kwargs):
        warnings.warn('{0.__module__}.{0.__name__} -> {0.__doc__}'.format(func), DeprecationWarning)
        return func(*args, **kwargs)
    return _inner

# vim: expandtab shiftwidth=4 tabstop=8 softtabstop=4 fileencoding=utf-8 textwidth=99
