#!/usr/bin/env python 
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

import copy
import inkex

class Interp(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option("-e", "--exponent",
                        action="store", type="float", 
                        dest="exponent", default=0.0,
                        help="values other than zero give non linear interpolation")
        self.OptionParser.add_option("-s", "--steps",
                        action="store", type="int", 
                        dest="steps", default=5,
                        help="number of interpolation steps")
        self.OptionParser.add_option("-m", "--method",
                        action="store", type="int", 
                        dest="method", default=2,
                        help="method of interpolation")
        self.OptionParser.add_option("-d", "--dup",
                        action="store", type="inkbool", 
                        dest="dup", default=True,
                        help="duplicate endpaths")    
        self.OptionParser.add_option("--style",
                        action="store", type="inkbool", 
                        dest="style", default=True,
                        help="try interpolation of some style properties")    
        self.OptionParser.add_option("--zsort",
                        action="store", type="inkbool",
                        dest="zsort", default=False,
                        help="use z-order instead of selection order")

    def effect(self):
        exponent = self.options.exponent
        if exponent>= 0:
            exponent = 1.0 + exponent
        else:
            exponent = 1.0/(1.0 - exponent)
        steps = [1.0/(self.options.steps + 1.0)]
        for i in range(self.options.steps - 1):
            steps.append(steps[0] + steps[-1])
        steps = [step**exponent for step in steps]
            
        paths = {}            
        styles = {}

        if self.options.zsort:
            # work around selection order swapping with Live Preview
            sorted_ids = pathmodifier.zSort(self.document.getroot(),self.selected.keys())
        else:
            # use selection order (default)
            sorted_ids = self.options.ids

        for id in sorted_ids:
            node = self.selected[id]
            if node.tag ==inkex.addNS('path','svg'):
                paths[id] = cubicsuperpath.parsePath(node.get('d'))
                styles[id] = dict(inkex.Style.parse_str(node.get('style')))
                trans = node.get('transform')
                if trans:
                    simpletransform.applyTransformToPath(simpletransform.parseTransform(trans), paths[id])
            else:
                sorted_ids.remove(id)

        for i in range(1,len(sorted_ids)):
            start = copy.deepcopy(paths[sorted_ids[i-1]])
            end = copy.deepcopy(paths[sorted_ids[i]])
            sst = copy.deepcopy(styles[sorted_ids[i-1]])
            est = copy.deepcopy(styles[sorted_ids[i]])
            basestyle = copy.deepcopy(sst)
            if basestyle.has_key('stroke-width'):
                basestyle['stroke-width'] = inkex.tweenstyleunit('stroke-width',sst,est,0)

            #prepare for experimental style tweening
            if self.options.style:
                dostroke = True
                dofill = True
                styledefaults = {'opacity':'1.0', 'stroke-opacity':'1.0', 'fill-opacity':'1.0',
                        'stroke-width':'1.0', 'stroke':'none', 'fill':'none'}
                for key in styledefaults.keys():
                    sst.setdefault(key,styledefaults[key])
                    est.setdefault(key,styledefaults[key])
                isnotplain = lambda x: not (x=='none' or x[:1]=='#')
                if isnotplain(sst['stroke']) or isnotplain(est['stroke']) or (sst['stroke']=='none' and est['stroke']=='none'):
                    dostroke = False
                if isnotplain(sst['fill']) or isnotplain(est['fill']) or (sst['fill']=='none' and est['fill']=='none'):
                    dofill = False
                if dostroke:
                    if sst['stroke']=='none':
                        sst['stroke-width'] = '0.0'
                        sst['stroke-opacity'] = '0.0'
                        sst['stroke'] = est['stroke'] 
                    elif est['stroke']=='none':
                        est['stroke-width'] = '0.0'
                        est['stroke-opacity'] = '0.0'
                        est['stroke'] = sst['stroke'] 
                if dofill:
                    if sst['fill']=='none':
                        sst['fill-opacity'] = '0.0'
                        sst['fill'] = est['fill'] 
                    elif est['fill']=='none':
                        est['fill-opacity'] = '0.0'
                        est['fill'] = sst['fill'] 

                    

            if self.options.method == 2:
                #subdivide both paths into segments of relatively equal lengths
                slengths, stotal = inkex.csplength(start)
                elengths, etotal = inkex.csplength(end)
                lengths = {}
                t = 0
                for sp in slengths:
                    for l in sp:
                        t += l / stotal
                        lengths.setdefault(t,0)
                        lengths[t] += 1
                t = 0
                for sp in elengths:
                    for l in sp:
                        t += l / etotal
                        lengths.setdefault(t,0)
                        lengths[t] += -1
                sadd = [k for (k,v) in lengths.iteritems() if v < 0]
                sadd.sort()
                eadd = [k for (k,v) in lengths.iteritems() if v > 0]
                eadd.sort()

                t = 0
                s = [[]]
                for sp in slengths:
                    if not start[0]:
                        s.append(start.pop(0))
                    s[-1].append(start[0].pop(0))
                    for l in sp:
                        pt = t
                        t += l / stotal
                        if sadd and t > sadd[0]:
                            while sadd and sadd[0] < t:
                                nt = (sadd[0] - pt) / (t - pt)
                                bezes = inkex.cspbezsplitatlength(s[-1][-1][:],start[0][0][:], nt)
                                s[-1][-1:] = bezes[:2]
                                start[0][0] = bezes[2]
                                pt = sadd.pop(0)
                        s[-1].append(start[0].pop(0))
                t = 0
                e = [[]]
                for sp in elengths:
                    if not end[0]:
                        e.append(end.pop(0))
                    e[-1].append(end[0].pop(0))
                    for l in sp:
                        pt = t
                        t += l / etotal
                        if eadd and t > eadd[0]:
                            while eadd and eadd[0] < t:
                                nt = (eadd[0] - pt) / (t - pt)
                                bezes = inkex.cspbezsplitatlength(e[-1][-1][:],end[0][0][:], nt)
                                e[-1][-1:] = bezes[:2]
                                end[0][0] = bezes[2]
                                pt = eadd.pop(0)
                        e[-1].append(end[0].pop(0))
                start = s[:]
                end = e[:]
            else:
                #which path has fewer segments?
                lengthdiff = inkex.numsegs(start) - inkex.numsegs(end)
                #swap shortest first
                if lengthdiff > 0:
                    start, end = end, start
                #subdivide the shorter path
                for x in range(abs(lengthdiff)):
                    maxlen = 0
                    subpath = 0
                    segment = 0
                    for y in range(len(start)):
                        for z in range(1, len(start[y])):
                            leng = inkex.bezlenapprx(start[y][z-1], start[y][z])
                            if leng > maxlen:
                                maxlen = leng
                                subpath = y
                                segment = z
                    sp1, sp2 = start[subpath][segment - 1:segment + 1]
                    start[subpath][segment - 1:segment + 1] = inkex.cspbezsplit(sp1, sp2)
                #if swapped, swap them back
                if lengthdiff > 0:
                    start, end = end, start
            
            #break paths so that corresponding subpaths have an equal number of segments
            s = [[]]
            e = [[]]
            while start and end:
                if start[0] and end[0]:
                    s[-1].append(start[0].pop(0))
                    e[-1].append(end[0].pop(0))
                elif end[0]:
                    s.append(start.pop(0))
                    e[-1].append(end[0][0])
                    e.append([end[0].pop(0)])
                elif start[0]:
                    e.append(end.pop(0))
                    s[-1].append(start[0][0])
                    s.append([start[0].pop(0)])
                else:
                    s.append(start.pop(0))
                    e.append(end.pop(0))
    
            if self.options.dup:
                steps = [0] + steps + [1]    
            #create an interpolated path for each interval
            group = inkex.etree.SubElement(self.current_layer,inkex.addNS('g','svg'))    
            for time in steps:
                interp = []
                #process subpaths
                for ssp,esp in zip(s, e):
                    if not (ssp or esp):
                        break
                    interp.append([])
                    #process superpoints
                    for sp,ep in zip(ssp, esp):
                        if not (sp or ep):
                            break
                        interp[-1].append([])
                        #process points
                        for p1,p2 in zip(sp, ep):
                            if not (sp or ep):
                                break
                            interp[-1][-1].append(inkex.interppoints(p1, p2, time))

                #remove final subpath if empty.
                if not interp[-1]:
                    del interp[-1]

                #basic style tweening
                if self.options.style:
                    basestyle['opacity'] = inkex.tweenstylefloat('opacity',sst,est,time)
                    if dostroke:
                        basestyle['stroke-opacity'] = inkex.tweenstylefloat('stroke-opacity',sst,est,time)
                        basestyle['stroke-width'] = inkex.tweenstyleunit('stroke-width',sst,est,time)
                        basestyle['stroke'] = inkex.tweenstylecolor('stroke',sst,est,time)
                    if dofill:
                        basestyle['fill-opacity'] = inkex.tweenstylefloat('fill-opacity',sst,est,time)
                        basestyle['fill'] = inkex.tweenstylecolor('fill',sst,est,time)
                attribs = {'style':str(inkex.Style(basestyle)),'d':cubicsuperpath.formatPath(interp)}
                new = inkex.etree.SubElement(group,inkex.addNS('path','svg'), attribs)

if __name__ == '__main__':
    e = Interp()
    e.affect()


# vim: expandtab shiftwidth=4 tabstop=8 softtabstop=4 fileencoding=utf-8 textwidth=99
