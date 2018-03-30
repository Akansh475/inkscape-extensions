# -*- coding: utf-8 -*-
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

import platform
PY3 = platform.python_version()[0] == '3' 

if PY3:
    unicode = str 
    basestring = str 

(X, Y) = range(2)

# a dictionary of all of the xmlns prefixes in a standard inkscape doc
NSS = { 
  u'sodipodi' :u'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd',
  u'cc'       :u'http://creativecommons.org/ns#',
  u'ccOLD'    :u'http://web.resource.org/cc/',
  u'svg'      :u'http://www.w3.org/2000/svg',
  u'dc'       :u'http://purl.org/dc/elements/1.1/',
  u'rdf'      :u'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
  u'inkscape' :u'http://www.inkscape.org/namespaces/inkscape',
  u'xlink'    :u'http://www.w3.org/1999/xlink',
  u'xml'      :u'http://www.w3.org/XML/1998/namespace'
}


