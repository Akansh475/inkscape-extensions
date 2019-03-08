#!/usr/bin/env python
# coding=utf-8
#
# Copyright (C) 2014 Martin Owens
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
Merges styles into class based styles and removes.
"""

from collections import defaultdict
import inkex

class Style(dict):
    """Controls the style/css mechanics for this effect"""
    def __init__(self, attr=None):
        super(Style, self).__init__()
        self.weights = defaultdict(int)
        self.total = []
        if attr:
            self.parse(attr)

    def parse(self, attr):
        """Parse a style attribute and store in this style"""
        for name, value in [a.split(':', 1) for a in attr.split(';') if ':' in a]:
            self[name.strip()] = value.strip()

    def entries(self):
        """Return the dictionary as a list of style entries"""
        return ["{}:{};".format(*item) for item in self.items()]

    def to_str(self, sep="\n    "):
        """Return the dictionary as a css text block"""
        return "    " + sep.join(self.entries())

    def __str__(self):
        return self.to_str()

    def css(self, cls):
        """Return this style as a css entry with class"""
        return ".%s {\n%s\n}" % (cls, str(self))

    def remove(self, keys):
        """Remove the given style keys"""
        for key in keys:
            self.pop(key, None)

    def add(self, other, elem):
        """Add the styles in the element"""
        self.total.append((other, elem))
        for name, value in other.items():
            if name not in self:
                self[name] = value
            if self[name] == value:
                self.weights[name] += 1

    def clean(self, threshold):
        """Removes any elements that aren't the same using a weighted threshold"""
        for attr in self.keys():
            if self.weights[attr] < len(self.total) - threshold:
                self.pop(attr)

    def all_matches(self):
        """Returns an iter for each added element who's style matches this style"""
        for (other, elem) in self.total:
            if self == other:
                yield (other, elem)

    def __eq__(self, o):
        """Not equals, prefer to overload 'in' but that doesn't seem possible"""
        for arg in self.keys():
            if arg in o and self[arg] != o[arg]:
                return False
        return True


def get_styles(document):
    """Returns all known style elements from the document"""
    nodes = []
    for node in document.getroot().iterchildren():
        if node.tag == inkex.addNS('style', 'svg'):
            return node
        nodes.append(node)
    ret = inkex.etree.SubElement(document.getroot(), 'style', {})
    # Reorder to make the style element FIRST
    for node in nodes:
        document.getroot().append(node)
    return ret


class MergeStyles(inkex.Effect):
    """Merge any styles which are the same for CSS"""
    def __init__(self):
        inkex.Effect.__init__(self)
        self.arg_parser.add_argument("-n", "--name", type=str, dest="name", default='',
                                     help="Name of selected element's common class")

    def effect(self):
        """Apply the style effect"""
        newclass = self.options.name
        elements = self.svg.selected.values()
        common = Style()
        threshold = 1

        for elem in elements:
            common.add(Style(elem.attrib['style']), elem)
        common.clean(threshold)

        if not common:
            return inkex.errormsg("There are no common styles between these elements.")

        styles = get_styles(self.document)
        styles.text = (styles.text or "") + "\n" + common.css(newclass)

        for (style, elem) in common.all_matches():
            style.remove(common.keys())
            elem.attrib['style'] = style.to_str("")

            olds = elem.attrib['class'].split() if 'class' in elem.attrib else []
            if newclass not in olds:
                olds.append(newclass)
            elem.attrib['class'] = ' '.join(olds)


if __name__ == '__main__':
    MergeStyles().run()
