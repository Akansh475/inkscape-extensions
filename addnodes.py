#!/usr/bin/env python 
#
# This extension either adds nodes to a path so that
#    a) no segment is longer than a maximum value 
#    or
#    b) so that each segment is divided into a given number of equal segments
#
# Copyright (C) 2005, 2007 Aaron Spike, aaron@ekips.org
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

import re
import math
import inkex

from inkex.utils import *

class SplitIt(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option("--segments",
                        action="store", type="int", 
                        dest="segments", default=2,
                        help="Number of segments to divide the path into")
        self.OptionParser.add_option("--max",
                        action="store", type="float", 
                        dest="max", default=2,
                        help="Number of segments to divide the path into")
        self.OptionParser.add_option("--method",
                        action="store", type="string", 
                        dest="method", default='',
                        help="The kind of division to perform")

    def effect(self):

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
                        
                        if self.options.method == 'bynum':
                            splits = self.options.segments
                        else:
                            splits = math.ceil(length/self.options.max)

                        for s in xrange(int(splits),1,-1):
                            new[-1][-1], next, sub[i] = cspbezsplitatlength(new[-1][-1], sub[i], 1.0/s)
                            new[-1].append(next[:])
                        new[-1].append(sub[i])
                        i+=1
                    
                node.set('d',cubicsuperpath.formatPath(new))

if __name__ == '__main__':
    e = SplitIt()
    e.affect()

# vim: expandtab shiftwidth=4 tabstop=8 softtabstop=4 fileencoding=utf-8 textwidth=99
