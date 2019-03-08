#!/usr/bin/env python
# coding=utf-8
"""
Copyright (C) 2010 Aurelio A. Heckert, aurium (a) gmail dot com

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
"""
# local library
from webslicer_effect import WebSlicer_Effect, is_empty
import inkex

class WebSlicer_CreateRect(WebSlicer_Effect):

    def __init__(self):
        WebSlicer_Effect.__init__(self)
        self.arg_parser.add_argument("--name")
        self.arg_parser.add_argument("--format", default="png")
        self.arg_parser.add_argument("--dpi", type=int)
        self.arg_parser.add_argument("--dimension")
        self.arg_parser.add_argument("--bg-color")
        self.arg_parser.add_argument("--quality", type=int)
        self.arg_parser.add_argument("--gif-type")
        self.arg_parser.add_argument("--palette-size", type=int)
        self.arg_parser.add_argument("--html-id")
        self.arg_parser.add_argument("--html-class")
        self.arg_parser.add_argument("--layout-disposition")
        self.arg_parser.add_argument("--layout-position-anchor")
        # inkscape param workaround
        self.arg_parser.add_argument("--tab")


    def unique_slice_name(self):
        name = self.options.name
        el = self.document.xpath( '//*[@id="'+name+'"]', namespaces=inkex.NSS )
        if len(el) > 0:
            if name[-3:] == '-00': name = name[:-3]
            num = 0
            num_s = '00'
            while len(el) > 0:
                num += 1
                num_s = str(num)
                if len(num_s)==1 : num_s = '0'+num_s
                el = self.document.xpath( '//*[@id="'+name+'-'+num_s+'"]',
                                          namespaces=inkex.NSS )
            self.options.name = name+'-'+num_s


    def validate_options(self):
        self.options.format = self.options.format.lower()
        if not is_empty( self.options.dimension ):
            self.options.dimension

    def effect(self):
        scale = self.svg.unittouu('1px')    # convert to document units
        self.validate_options()
        layer = self.get_slicer_layer(True)
        #TODO: get selected elements to define location and size
        rect = inkex.etree.SubElement(layer, 'rect')
        if is_empty(self.options.name):
            self.options.name = 'slice-00'
        self.unique_slice_name()
        rect.set('id', self.options.name)
        rect.set('fill', 'red')
        rect.set('opacity', '0.5')
        rect.set('x', str(-scale*100))
        rect.set('y', str(-scale*100))
        rect.set('width', str(scale*200))
        rect.set('height', str(scale*200))
        desc = inkex.etree.SubElement(rect, 'desc')
        conf_txt = "format:"+ self.options.format +"\n"
        if not is_empty(self.options.dpi):
            conf_txt += "dpi:"     + str(self.options.dpi) +"\n"
        if not is_empty(self.options.html_id):
            conf_txt += "html-id:" + self.options.html_id
        desc.text = self.get_conf_text_from_list( self.get_conf_list() )


    def get_conf_list(self):
        conf_list = [ 'format' ]
        if self.options.format == 'gif':
            conf_list.extend( [ 'gif_type', 'palette_size' ] )
        if self.options.format == 'jpg':
            conf_list.extend( [ 'quality' ] )
        conf_list.extend( [
                'dpi', 'dimension',
                'bg_color', 'html_id', 'html_class',
                'layout_disposition', 'layout_position_anchor'
            ] )
        return conf_list



if __name__ == '__main__':
    WebSlicer_CreateRect().run()
