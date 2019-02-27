# coding=utf-8
#
# Copyright (C) 2010 Nick Drobchenko, nick@cnc-club.ru
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
"""
Basic common utility functions for calculated things
"""
from __future__ import absolute_import, print_function, unicode_literals


import os
import sys

from argparse import ArgumentTypeError

import platform
PY3 = platform.python_version()[0] == '3'

(X, Y) = range(2)

if PY3:
    unicode = str # pylint: disable=redefined-builtin,invalid-name
    basestring = str # pylint: disable=redefined-builtin,invalid-name

# a dictionary of all of the xmlns prefixes in a standard inkscape doc
NSS = {
    'sodipodi' :'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd',
    'cc'       :'http://creativecommons.org/ns#',
    'ccOLD'    :'http://web.resource.org/cc/',
    'svg'      :'http://www.w3.org/2000/svg',
    'dc'       :'http://purl.org/dc/elements/1.1/',
    'rdf'      :'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'inkscape' :'http://www.inkscape.org/namespaces/inkscape',
    'xlink'    :'http://www.w3.org/1999/xlink',
    'xml'      :'http://www.w3.org/XML/1998/namespace'
}
SSN = dict((b, a) for (a, b) in NSS.items())

def inkbool(value):
    """Turn a boolean string into a python boolean"""
    if value.upper() == 'TRUE':
        return True
    elif value.upper() == 'FALSE':
        return False

def debug(what):
    """Print debug message if debugging is switched on"""
    sys.stderr.write(unicode(what) + "\n")
    return what

def errormsg(msg):
    """Intended for end-user-visible error messages.

       (Currently just writes to stderr with an appended newline, but could do
       something better in future: e.g. could add markup to distinguish error
       messages from status messages or debugging output.)

       Note that this should always be combined with translation:

         import inkex
         ...
         inkex.errormsg(_("This extension requires two selected paths."))
    """
    sys.stderr.write(unicode(msg) + "\n")

class AbortExtension(Exception):
    """Raised to print a message to the user without backtrace"""
    def write(self):
        """write the error message out to the user"""
        errormsg(str(self))

class DependencyError(NotImplementedError):
    """Raised when we need an external python module that isn't available"""

def to(kind): # pylint: disable=invalid-name
    """
    Decorator which will turn a generator into a list, tuple or other object type.
    """
    def _inner(call):
        def _outer(*args, **kw):
            return kind(call(*args, **kw))
        return _outer
    return _inner

def strargs(string, kind=float):
    """Returns a list of floats from a string with commas or space separators"""
    return [kind(val) for val in string.replace(',', ' ').split()]

def addNS(tag, ns=None): # pylint: disable=invalid-name
    """Add a known namespace to a name for use with lxml"""
    if tag.startswith('{') and ns:
        _, tag = removeNS(tag)
    if not tag.startswith('{'):
        if ':' in tag:
            (ns, tag) = tag.rsplit(':', 1)
        if ns in NSS:
            ns = NSS[ns]
        if ns is not None:
            return "{%s}%s" % (ns, tag)
    return tag

def removeNS(name, url=False): # pylint: disable=invalid-name
    """The reverse of addNS, finds any namespace and returns tuple (ns, tag)"""
    if name:
        if name[0] == '{':
            (nsp, tag) = name[1:].split('}', 1)
            return (nsp, tag) if url else (SSN.get(nsp, 'svg'), tag)
        if ':' in name:
            (nsp, tag) = name.rsplit(':', 1)
            return (NSS[nsp], tag) if url else (nsp, tag)
    return (NSS['svg'], name) if url else ('svg', name)

class classproperty(object): # pylint: disable=invalid-name, too-few-public-methods
    """Combine classmethod and property decorators"""
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, owner):
        return self.func(owner)

def filename_arg(name):
    """Existing file to read or option used in script arguments"""
    filename = os.path.abspath(os.path.expanduser(name))
    if not os.path.isfile(filename):
        raise ArgumentTypeError("File not found: {}".format(name))
    return filename


