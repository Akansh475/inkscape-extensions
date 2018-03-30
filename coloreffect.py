#!/usr/bin/env python 
#
# Copyright (C) 2006 Jos Hirth, kaioa.com
# Copyright (C) 2007 Aaron C. Spike
# Copyright (C) 2009 Monash University
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

import sys
import copy
import random

import inkex

color_props_fill = ('fill', 'stop-color',  'flood-color', 'lighting-color')
color_props_stroke = ('stroke',)
opacity_props = ('opacity',) #'stop-opacity', 'fill-opacity', 'stroke-opacity' don't work with clones
color_props = color_props_fill + color_props_stroke


class ColorEffect(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.visited = []

    def effect(self):
        if len(self.selected)==0:
            self.getAttribs(self.document.getroot())
        else:
            for id,node in self.selected.items():
                self.getAttribs(node)

    def getAttribs(self,node):
        self.changeStyle(node)
        for child in node:
            self.getAttribs(child)

    def changeStyle(self,node):
        for attr in color_props:
                val = node.get(attr)
                if val:
                        new_val = self.process_prop(val)
                        if new_val != val:
                                node.set(attr, new_val)

        if node.attrib.has_key('style'):
            return self._style(node)

    def _style(self, node):
        # References for style attribute:
        # http://www.w3.org/TR/SVG11/styling.html#StyleAttribute,
        # http://www.w3.org/TR/CSS21/syndata.html
        #
        # The SVG spec is ambiguous as to how style attributes should be parsed.
        # For example, it isn't clear whether semicolons are allowed to appear
        # within strings or comments, or indeed whether comments are allowed to
        # appear at all.
        #
        # The processing here is just something simple that should usually work,
        # without trying too hard to get everything right.
        # (Won't work for the pathological case that someone escapes a property
        # name, probably does the wrong thing if colon or semicolon is used inside
        # a comment or string value.)
        style = node.get('style') # fixme: this will break for presentation attributes!
        if style:
            #inkex.debug('old style:'+style)
            declarations = style.split(';')
            opacity_in_style = False
            for i,decl in enumerate(declarations):
                parts = decl.split(':', 2)
                if len(parts) == 2:
                    (prop, val) = parts
                    prop = prop.strip().lower()
                    if prop in color_props:
                        val = val.strip()
                        new_val = self.process_prop(val)
                        if new_val != val:
                            declarations[i] = prop + ':' + new_val
                    elif prop in opacity_props:
                        opacity_in_style = True
                        val = val.strip()
                        new_val = self.process_prop(val)
                        if new_val != val:
                            declarations[i] = prop + ':' + new_val
            if not opacity_in_style:
                new_val = self.process_prop("1")
                declarations.append('opacity' + ':' + new_val)
            #inkex.debug('new style:'+';'.join(declarations))
            node.set('style', ';'.join(declarations))

    def process_prop(self, col):
        #inkex.debug('got:'+col+str(type(col)))
        if inkex.isColor(col):
            c=inkex.parseColor(col)
            col='#'+self.colmod(c[0], c[1], c[2])
            #inkex.debug('made:'+col)
        elif col.startswith('url(#'):
            id = col[len('url(#'):col.find(')')]
            newid = '%s-%d' % (id, int(random.random() * 1000))
            #inkex.debug('ID:' + id )
            path = '//*[@id="%s"]' % id
            for node in self.document.xpath(path, namespaces=inkex.NSS):
                self.process_gradient(node, newid)
            col = 'url(#%s)' % newid
        # what remains should be opacity
        else:
            col = self.opacmod(col)
            
        #inkex.debug('col:'+str(col))
        return col

    def process_gradient(self, node, newid):
        #if node.hasAttributes():
             #this_id=node.getAttribute('id')
             #if this_id in self.visited:
                 ## prevent multiple processing of the same gradient if it is used by more than one selected object
                 ##inkex.debug("already had: " + this_id)
                 #return
             #self.visited.append(this_id)
             #inkex.debug("visited: " + str(self.visited))
        newnode = copy.deepcopy(node)
        newnode.set('id', newid)
        node.getparent().append(newnode)
        self.changeStyle(newnode)
        for child in newnode:
            self.changeStyle(child)
        xlink = inkex.addNS('href','xlink')
        if newnode.attrib.has_key(xlink):
            href=newnode.get(xlink)
            if href.startswith('#'):
                id = href[len('#'):len(href)]
                #inkex.debug('ID:' + id )
                newhref = '%s-%d' % (id, int(random.random() * 1000))
                newnode.set(xlink, '#%s' % newhref)
                path = '//*[@id="%s"]' % id
                for node in self.document.xpath(path, namespaces=inkex.NSS):
                    self.process_gradient(node, newhref)
 
    def colmod(self,r,g,b):
        pass
    
    def opacmod(self, opacity):
        return opacity

# vi: set autoindent shiftwidth=2 tabstop=8 expandtab softtabstop=2 :
