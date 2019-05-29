#!/usr/bin/env python

# Copyright (C) 2019 Gemy Cedric Activdesign.eu
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
# local library
import inkwebeffect
import inkex


class InkWebIMockup(inkwebeffect.InkWebEffect):

    def __init__(self):
        super(InkWebIMockup, self).__init__()
        self.arg_parser.add_argument("--when", type=str, dest="when", default="onclick",
                                     help="Event that will trigger the action")
        self.arg_parser.add_argument("--tab", type=str, dest="tab",
                                     help="The selected UI-tab when OK was pressed")

    def effect(self):
      self.ensureInkWebSupport()

      if len(self.options.ids) < 2:
        raise inkex.AbortExtension("You must select at least two elements. The last one is the object you want to go to")


      elFrom = []
      for selId in self.options.ids[:-1]:
        elFrom.append( self.svg.selected[selId] )

      evCode = "InkWeb.moveViewbox({from:this, " + \
                                   "to:'"+ self.options.ids[-1] +"'})" #+ \
      elEvCode = ""
      for el in elFrom:
        prevEvCode = el.get( self.options.when )
        if prevEvCode == None: prevEvCode = ""
        elEvCode = evCode +";"+ prevEvCode
        el.set( self.options.when, elEvCode )

if __name__ == '__main__':
    e = InkWebIMockup().run()

