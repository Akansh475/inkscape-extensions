#!/usr/bin/env python
# coding=utf-8
#
# Copyright (C) 2006 Jean-Francois Barraud, barraud@math.univ-lille1.fr
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
# barraud@math.univ-lille1.fr
#
"""
This code defines a basic class (PathModifier) of effects whose purpose is
to somehow deform given objects: one common tasks for all such effect is to
convert shapes, groups, clones to paths. The class has several functions to
make this (more or less!) easy.
As an example, a second class (Diffeo) is derived from it,
to implement deformations of the form X=f(x,y), Y=g(x,y)...

TODO: Several handy functions are defined, that might in fact be of general
interest and that should be shipped out in separate files...
"""

import copy

import inkex
from inkex.localization import _
from inkex.elements import PathElement, Group, Use
from inkex.deprecated import deprecate

@deprecate
def zSort(inNode, idList):
    """self.svg.get_z_selected()"""
    sortedList = []
    theid = inNode.get("id")
    if theid in idList:
        sortedList.append(theid)
    for child in inNode:
        if len(sortedList) == len(idList):
            break
        sortedList += zSort(child, idList)
    return sortedList


class PathModifier(inkex.EffectExtension):
    """Select list manipulation"""
    def duplicateNodes(self, aList):
        clones = {}
        for id, node in aList.items():
            clone = copy.deepcopy(node)
            # !!!--> should it be given an id?
            # seems to work without this!?!
            myid = node.tag.split('}')[-1]
            clone.set("id", self.svg.get_unique_id(myid))
            node.getparent().append(clone)
            clones[clone.get("id")] = clone
        return clones

    def expandGroups(self, aList, transferTransform=True):
        for id, node in aList.items():
            if node.tag == inkex.addNS('g', 'svg') or node.tag == 'g':
                mat = node.transform
                for child in node:
                    if transferTransform:
                        child.transform *= mat
                    aList.update(self.expandGroups({child.get('id'): child}))
                if transferTransform and node.get("transform"):
                    del node.attrib["transform"]
                del aList[id]
        return aList

    def expandGroupsUnlinkClones(self, aList, transferTransform=True, doReplace=True):
        for elem_id, node in aList.items():
            if isinstance(node, Group):
                self.expandGroups(aList, transferTransform)
                self.expandGroupsUnlinkClones(aList, transferTransform, doReplace)
                # Hum... not very efficient if there are many clones of groups...

            elif isinstance(node, Use):
                refnode = node.href
                newnode = self.unlinkClone(node, doReplace)
                del aList[elem_id]

                style = dict(inkex.Style.parse_str(node.get('style') or ""))
                refstyle = dict(inkex.Style.parse_str(refnode.get('style') or ""))
                style.update(refstyle)
                newnode.set('style', str(inkex.Style(style)))

                newid = newnode.get('id')
                aList.update(self.expandGroupsUnlinkClones({newid: newnode}, transferTransform, doReplace))
        return aList

    def recursNewIds(self, node):
        if node.get('id'):
            node.set('id', self.svg.get_unique_id(node.tag))
        for child in node:
            self.recursNewIds(child)

    def unlinkClone(self, node, doReplace):
        if node.tag == inkex.addNS('use', 'svg') or node.tag == 'use':
            newNode = copy.deepcopy(node.href)
            self.recursNewIds(newNode)
            newNode.transform *= node.transform

            if doReplace:
                parent = node.getparent()
                parent.insert(parent.index(node), newNode)
                parent.remove(node)

            return newNode
        else:
            raise AssertionError("Only clones can be unlinked...")

    ################################
    # -- Object conversion ----------
    ################################

    def rectToPath(self, node, doReplace=True):
        if node.tag == inkex.addNS('rect', 'svg'):
            x = float(node.get('x'))
            y = float(node.get('y'))
            # FIXME: no exception anymore and sometimes just one
            try:
                rx = float(node.get('rx'))
                ry = float(node.get('ry'))
            except:
                rx = 0
                ry = 0
            w = float(node.get('width'))
            h = float(node.get('height'))
            d = 'M %f,%f ' % (x + rx, y)
            d += 'L %f,%f ' % (x + w - rx, y)
            d += 'A %f,%f,%i,%i,%i,%f,%f ' % (rx, ry, 0, 0, 1, x + w, y + ry)
            d += 'L %f,%f ' % (x + w, y + h - ry)
            d += 'A %f,%f,%i,%i,%i,%f,%f ' % (rx, ry, 0, 0, 1, x + w - rx, y + h)
            d += 'L %f,%f ' % (x + rx, y + h)
            d += 'A %f,%f,%i,%i,%i,%f,%f ' % (rx, ry, 0, 0, 1, x, y + h - ry)
            d += 'L %f,%f ' % (x, y + ry)
            d += 'A %f,%f,%i,%i,%i,%f,%f ' % (rx, ry, 0, 0, 1, x + rx, y)

            newnode = PathElement()
            newnode.set('d', d)
            newnode.set('id', self.svg.get_unique_id('path'))
            newnode.set('style', node.get('style'))
            nnt = node.get('transform')
            if nnt:
                newnode.set('transform', nnt)
                newnode.apply_transform()
            if doReplace:
                parent = node.getparent()
                parent.insert(parent.index(node), newnode)
                parent.remove(node)
            return newnode

    def groupToPath(self, node, doReplace=True):
        if node.tag == inkex.addNS('g', 'svg'):
            newNode = PathElement()
            self.svg.get_current_layer().append(newNode)

            newstyle = dict(inkex.Style.parse_str(node.get('style') or ""))
            newp = []
            for child in node:
                childstyle = dict(inkex.Style.parse_str(child.get('style') or ""))
                childstyle.update(newstyle)
                newstyle.update(childstyle)
                childAsPath = self.objectToPath(child, False)
                newp += childAsPath.path.to_superpath()
            newNode.path = newp
            newNode.style = newstyle

            self.svg.get_current_layer().remove(newNode)
            if doReplace:
                parent = node.getparent()
                parent.insert(parent.index(node), newNode)
                parent.remove(node)

            return newNode
        else:
            raise AssertionError('Node is not a group')

    def objectToPath(self, node, doReplace=True):
        # --TODO: support other object types!!!!
        if node.tag == inkex.addNS('rect', 'svg'):
            return self.rectToPath(node, doReplace)
        if node.tag == inkex.addNS('g', 'svg'):
            return self.groupToPath(node, doReplace)
        elif node.tag == inkex.addNS('path', 'svg') or node.tag == 'path':
            # remove inkscape attributes, otherwise any modif of 'd' will be discarded!
            for attName in list(node.attrib.keys()):
                if ("sodipodi" in attName) or ("inkscape" in attName):
                    del node.attrib[attName]
            node.apply_transform()
            return node
        elif node.tag == inkex.addNS('use', 'svg') or node.tag == 'use':
            newNode = self.unlinkClone(node, doReplace)
            return self.objectToPath(newNode, doReplace)
        else:
            inkex.errormsg(_("Please first convert objects to paths!  (Got [%s].)") % node.tag)
            return None

    def objectsToPaths(self, aList, doReplace=True):
        newSelection = {}
        for id, node in list(aList.items()):
            newnode = self.objectToPath(node, doReplace)
            del aList[id]
            aList[newnode.get('id')] = newnode

    ################################
    # -- Action ----------
    ################################

    def effect(self):
        raise NotImplementedError("overwrite this method in subclasses")
        # self.duplicateNodes(self.selected)
        # self.expandGroupsUnlinkClones(self.selected, True)
        self.objectsToPaths(self.svg.selected, True)
        self.bbox = self.svg.get_selected_bbox()
        for node in self.svg.get_selected(PathElement):
            path = node.path.to_superpath()
            # do what ever you want with "path"!
            node.path = path


class Diffeo(PathModifier):
    def applyDiffeo(self, bpt, vects=()):
        # bpt is a base point and for v in vectors, v'=v-p is a tangent vector at bpt.
        # Defaults to identity!
        for v in vects:
            v[0] -= bpt[0]
            v[1] -= bpt[1]

        # -- your transformations go here:
        # x,y=bpt
        # bpt[0]=f(x,y)
        # bpt[1]=g(x,y)
        # for v in vects:
        #    vx,vy=v
        #    v[0]=df/dx(x,y)*vx+df/dy(x,y)*vy
        #    v[1]=dg/dx(x,y)*vx+dg/dy(x,y)*vy
        #
        # -- !caution! y-axis is pointing downward!

        for v in vects:
            v[0] += bpt[0]
            v[1] += bpt[1]

    def effect(self):
        self.expandGroupsUnlinkClones(self.svg.selected, True)
        self.expandGroups(self.svg.selected, True)
        self.objectsToPaths(self.svg.selected, True)
        self.bbox = self.svg.get_selected_bbox()
        for node in self.svg.get_selected(PathElement):
            path = node.path.to_superpath()
            for sub in path:
                for ctlpt in sub:
                    self.applyDiffeo(ctlpt[1], (ctlpt[0], ctlpt[2]))
            node.path = path

if __name__ == '__main__':
    Diffeo().run()
