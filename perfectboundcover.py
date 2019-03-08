#!/usr/bin/env python
# coding=utf-8
'''
Copyright (C) 2007 John Bintz, jcoswell@cosellproductions.org

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
'''
import inkex
from inkex import inkbool


def caliper_to_ppi(caliper):
    return 2 / caliper

def bond_weight_to_ppi(bond_weight):
    return caliper_to_ppi(bond_weight * .0002)

def points_to_ppi(points):
    return caliper_to_ppi(points / 1000.0)

class PerfectBoundCover(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.arg_parser.add_argument("--width",
                         type=float,
                        dest="width", default=6.0,
                        help="cover width (in)")
        self.arg_parser.add_argument("--height",
                         type=float,
                        dest="height", default=9.0,
                        help="cover height (in)")
        self.arg_parser.add_argument("--pages",
                         type=int,
                        dest="pages", default=64,
                        help="number of pages")
        self.arg_parser.add_argument("--paperthicknessmeasurement",
                         type=str,
                        dest="paperthicknessmeasurement", default=100.0,
                        help="paper thickness measurement")
        self.arg_parser.add_argument("--paperthickness",
                         type=float,
                        dest="paperthickness", default=0.0,
                        help="paper thickness")
        self.arg_parser.add_argument("--coverthicknessmeasurement",
                         type=str,
                        dest="coverthicknessmeasurement", default=100.0,
                        help="cover thickness measurement")
        self.arg_parser.add_argument("--coverthickness",
                         type=float,
                        dest="coverthickness", default=0.0,
                        help="cover thickness")
        self.arg_parser.add_argument("--bleed",
                         type=float,
                        dest="bleed", default=0.25,
                        help="cover bleed (in)")
        self.arg_parser.add_argument("--removeguides",
                         type=inkbool,
                        dest="removeguides", default=False,
                        help="remove guides")
        self.arg_parser.add_argument("--book",
                         type=str,
                        dest="book", default=False,
                        help="dummy")
        self.arg_parser.add_argument("--cover",
                         type=str,
                        dest="cover", default=False,
                        help="dummy")
        self.arg_parser.add_argument("--paper",
                         type=str,
                        dest="paper", default=False,
                        help="dummy")
        self.arg_parser.add_argument("--warning",
                         type=str,
                        dest="warning", default=False,
                        help="dummy")
    def effect(self):
        switch = {
          "ppi": lambda x: x,
          "caliper": lambda x: caliper_to_ppi(x),
          "bond_weight": lambda x: bond_weight_to_ppi(x),
          "points": lambda x: points_to_ppi(x),
          "width": lambda x: x
        }

        if self.options.paperthickness > 0:
            if self.options.paperthicknessmeasurement == "width":
                paper_spine = self.options.paperthickness
            else:
                paper_spine = self.options.pages / switch[self.options.paperthicknessmeasurement](self.options.paperthickness)
        else:
            paper_spine = 0

        if self.options.coverthickness > 0:
            if self.options.coverthicknessmeasurement == "width":
                cover_spine = self.options.coverthickness
            else:
                cover_spine = 4.0 / switch[self.options.coverthicknessmeasurement](self.options.coverthickness)
        else:
            cover_spine = 0

        spine_width = paper_spine + cover_spine

        document_width = (self.options.bleed + self.options.width * 2) + spine_width
        document_height = self.options.bleed * 2 + self.options.height

        root = self.document.getroot()

        root.set("width", "%sin" % document_width)
        root.set("height", "%sin" % document_height)

        guides = []

        guides.append(["horizontal", self.options.bleed])
        guides.append(["horizontal", document_height - self.options.bleed])
        guides.append(["vertical", self.options.bleed])
        guides.append(["vertical", document_width - self.options.bleed])
        guides.append(["vertical", (document_width / 2) - (spine_width / 2)])
        guides.append(["vertical", (document_width / 2) + (spine_width / 2)])

        namedview = self.document.xpath('/svg:svg/sodipodi:namedview', namespaces=inkex.NSS)
        if namedview:
            if self.options.removeguides == True:
                for node in self.document.xpath('/svg:svg/sodipodi:namedview/sodipodi:guide', namespaces=inkex.NSS):
                    parent = node.getparent()
                    parent.remove(node)
            for guide in guides:
                newguide = inkex.etree.Element(inkex.addNS('guide','sodipodi'))
                newguide.set("orientation", guide[0])
                newguide.set("position", "%f" % (guide[1] * 96))
                namedview[0].append(newguide)

        '''
        for id, node in self.selected.items():
            if node.tag == inkex.addNS('path','svg'):
                p = cubicsuperpath.parsePath(node.get('d'))
                
                #lens, total = csplength(p)
                #avg = total/numlengths(lens)
                #inkex.debug("average segment length: %s" % avg)

                new = []
                for sub in p:
                    new.append([sub[0][:]])
                    i = 1
                    while i <= len(sub)-1:
                        length = cspseglength(new[-1][-1], sub[i])
                        if length > self.options.max:
                            splits = math.ceil(length/self.options.max)
                            for s in xrange(int(splits),1,-1):
                                new[-1][-1], next, sub[i] = cspbezsplitatlength(new[-1][-1], sub[i], 1.0/s)
                                new[-1].append(next[:])
                        new[-1].append(sub[i])
                        i+=1
                    
                node.set('d',cubicsuperpath.formatPath(new))
            '''


if __name__ == '__main__':
    PerfectBoundCover().run()


