#!/usr/bin/env python
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

import os
import sys

from argparse import ArgumentTypeError

from itertools import tee
from .const import NSS, PY3

def debug(what):
    """Print debug message if debugging is switched on"""
    sys.stderr.write(str(what) + "\n")
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
    if PY3:
        sys.stderr.write(msg + "\n")
    elif isinstance(msg, unicode):
        sys.stderr.write(msg.encode("utf-8") + "\n")
    else:
        sys.stderr.write((unicode(msg, "utf-8", errors='replace') + "\n").encode("utf-8"))

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

def addNS(tag, ns=None): # pylint: disable=invalid-name
    """Add a known namespace to a name for use with lxml"""
    val = tag
    if ns is not None and len(ns) > 0 and ns in NSS and len(tag) > 0 and tag[0] != '{':
        val = "{%s}%s" % (NSS[ns], tag)
    return val

def pairwise(iterable):
    "Iterate over a list with overlapping pairs (see itertools recipies)"
    first, then = tee(iterable)
    next(then, None)
    return zip(first, then)

def filename_arg(name):
    """Existing file to read or option used in script arguments"""
    filename = os.path.abspath(os.path.expanduser(name))
    if not os.path.isfile(filename):
        raise ArgumentTypeError("File not found: {}".format(name))
    # TODO: File handle is kept open forever!
    return open(filename, 'r')


