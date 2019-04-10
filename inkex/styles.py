# coding=utf-8
#
# Copyright (C) 2005 Aaron Spike, aaron@ekips.org
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
Two simple functions for working with inline css
and some color handling on top.
"""

from collections import OrderedDict


class Style(OrderedDict):
    """A list of style directives"""

    def __init__(self, style=None, callback=None, **kw):
        self.callback = None
        style = style or kw
        if isinstance(style, str):
            style = self.parse_str(style)
        # Should accept dict, Style, parsed string, list etc.
        super(Style, self).__init__(style)
        self.callback = callback

    @staticmethod
    def parse_str(style):
        """Create a dictionary from the value of an inline style attribute"""
        if style is None:
            style = ""
        for directive in style.split(';'):
            if ':' in directive:
                (name, value) = directive.split(':', 1)
                # FUTURE: Parse value here for extra functionality
                yield (name.strip().lower(), value.strip())

    def __str__(self):
        """Format an inline style attribute from a dictionary"""
        return ";".join(["{0}:{1}".format(*seg) for seg in self.items()])

    def __add__(self, other):
        """Add two styles together to get a third, composing them"""
        ret = self.copy()
        ret.update(Style(other))
        return ret

    def __iadd__(self, other):
        """Add style to this style, the same as style.update(dict)"""
        self.update(other)
        return self

    def update(self, other):
        """Make sure callback is called when updating"""
        super(Style, self).update(Style(other))
        if self.callback is not None:
            self.callback(self)

    def __setitem__(self, key, value):
        super(Style, self).__setitem__(key, value)
        if self.callback is not None:
            self.callback(self)
