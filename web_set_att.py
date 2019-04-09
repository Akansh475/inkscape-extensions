#!/usr/bin/env python
#
# Copyright (C) 2009 Aurelio A. Heckert, aurium (a) gmail dot com
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
This effect adds a feature visible (or usable) only on a SVG enabled web
browser (like Firefox). This effect sets one or more attributes in the second
selected element, when a defined event occurs on the first selected element.
If you want to set more than one attribute, you must separate this with a space,
and only with aspace.
"""

# local library
import inkwebeffect
from inkex.localize import _

class InkWebTransmitAtt(inkwebeffect.InkWebEffect):

    def __init__(self):
        super(InkWebTransmitAtt, self).__init__()
        self.arg_parser.add_argument("-a", "--att",
                                     type=str,
                                     dest="att", default="fill",
                                     help="Attribute to set.")
        self.arg_parser.add_argument("-v", "--val",
                                     type=str,
                                     dest="val", default="red",
                                     help="Values to set.")
        self.arg_parser.add_argument("-w", "--when",
                                     type=str,
                                     dest="when", default="onclick",
                                     help="When it must to set?")
        self.arg_parser.add_argument("-c", "--compatibility",
                                     type=str,
                                     dest="compatibility", default="append",
                                     help="Compatibility with previews code to this event.")
        self.arg_parser.add_argument("-t", "--from-and-to",
                                     type=str,
                                     dest="from_and_to", default="g-to-one",
                                     help='Who transmit to Who? "g-to-one" All set the last. "one-to-g" The first set all.')
        self.arg_parser.add_argument("--tab",
                                     type=str,
                                     dest="tab",
                                     help="The selected UI-tab when OK was pressed")

    def effect(self):
        self.ensureInkWebSupport()

        if len(self.options.ids) < 2:
            return inkwebeffect.inkex.errormsg(_("You must select at least two elements."))

        elFrom = []
        idTo = []
        if self.options.from_and_to == "g-to-one":
            # All set the last
            for selId in self.options.ids[:-1]:
                elFrom.append(self.svg.selected[selId])
            idTo.append(self.options.ids[-1])
        else:
            # The first set all
            elFrom.append(self.selected[self.options.ids[0]])
            for selId in self.options.ids[1:]:
                idTo.append(selId)

        evCode = "InkWeb.setAtt({{el:['{}'], att:'{}', val:'{}'}})".format("','".join(idTo),
                                                                         self.options.att,
                                                                         self.options.val)
        for el in elFrom:
            prevEvCode = el.get(self.options.when)
            if prevEvCode is None:
                prevEvCode = ""

            if self.options.compatibility == 'append':
                elEvCode = prevEvCode + ";\n" + evCode
            if self.options.compatibility == 'prepend':
                elEvCode = evCode + ";\n" + prevEvCode

            el.set(self.options.when, elEvCode)


if __name__ == '__main__':
    InkWebTransmitAtt().run()
