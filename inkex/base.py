# coding=utf-8
#
# Copyright (c) 2018 - Martin Owens <doctormo@gmail.com>
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
The ultimate base functionality for every inkscape extension.
"""
from __future__ import absolute_import, print_function, unicode_literals

import os
import sys
import copy
import shutil

from argparse import ArgumentParser
from lxml import etree

from .utils import filename_arg, AbortExtension
from .svg import SVG_PARSER

stdout = sys.stdout
if sys.version_info[0] == 3:  #PY3
    unicode = str  # pylint: disable=redefined-builtin,invalid-name
    basestring = str  # pylint: disable=redefined-builtin,invalid-name
    stdout = sys.stdout.buffer


class InkscapeExtension(object):
    """
    The base class extension, provides argument parsing and basic
    variable handling features.
    """

    def __init__(self):
        self.file_io = None
        self.options = None
        self.document = None
        self.arg_parser = ArgumentParser(description=self.__doc__)

        self.arg_parser.add_argument(
            "input_file", nargs="?", metavar="INPUT_FILE", type=filename_arg,
            help="Filename of the input file (default is stdin)", default=None)

        self.arg_parser.add_argument(
            "--output", type=str, default=None,
            help="Optional output filename for saving the result (default is stdout).")

        self.add_arguments(self.arg_parser)

    def add_arguments(self, pars):
        """Add any extra arguments to your extension handle, use:

        def add_arguments(self, pars):
            pars.add_argument("--num-cool-things", type=int, default=3)
            pars.add_argument("--pos-in-doc", type=str, default="doobry")
        """
        pass  # No extra arguments by default so super is not required

    def run(self, args=None, output=None):
        """Main entrypoint for any Inkscape Extension"""
        try:
            if args is None:
                args = sys.argv[1:]

            self.options = self.arg_parser.parse_args(args)
            if self.options.input_file is None:
                self.options.input_file = sys.stdin

            if self.options.output is None:
                # assert output
                self.options.output = (output or stdout)

            try:
                self.load_raw()
                ret = self.effect()
                self.save_raw(ret)
            except AbortExtension as err:
                err.write()
                ret = False
        except Exception:
            self.clean_up()
            raise
        else:
            self.clean_up()

    def load_raw(self):
        """Load the input stream or filename, save everything to self"""
        if isinstance(self.options.input_file, (str, unicode)):
            self.file_io = open(self.options.input_file, 'rb')
            self.document = self.load(self.file_io)
        else:
            self.document = self.load(self.options.input_file)

    def save_raw(self, ret):
        """Save to the output steam, use everything from self"""
        if self.has_changed(ret):
            if isinstance(self.options.output, (str, unicode)):
                with open(self.options.output, 'wb') as stream:
                    self.save(stream)
            else:
                self.save(self.options.output)

    def load(self, stream):
        """Takes the input stream and creates a document for parsing"""
        raise NotImplementedError("No input handle for {}".format(self.name))

    def save(self, stream):
        """Save the given document to the output file"""
        raise NotImplementedError("No output handle for {}".format(self.name))

    def effect(self):
        """Apply some effects on the document or local context"""
        raise NotImplementedError("No effect handle for {}".format(self.name))

    def has_changed(self, ret): # pylint: disable=no-self-use
        """Return true if the output should be saved"""
        return ret is not False

    def clean_up(self):
        """Clean up any open handles and other items"""
        if self.file_io is not None:
            self.file_io.close()

    @property
    def name(self):
        """Return a fixed name for this extension"""
        return type(self).__name__


class TempDirMixin(object):
    """
    Provide a temporary directory for extensions to stash files.
    """
    dir_suffix = ''
    dir_prefix = 'inktmp'

    def __init__(self, *args, **kwargs):
        self.tempdir = None
        super(TempDirMixin, self).__init__(*args, **kwargs)

    def load_raw(self):
        """Create the temporary directory"""
        from tempfile import mkdtemp
        self.tempdir = mkdtemp(self.dir_suffix, self.dir_prefix, None)
        super(TempDirMixin, self).load_raw()

    def clean_up(self):
        """Delete the temporary directory"""
        if self.tempdir and os.path.isdir(self.tempdir):
            shutil.rmtree(self.tempdir)
        super(TempDirMixin, self).clean_up()


class SvgInputMixin(object):  # pylint: disable=too-few-public-methods
    """
    Expects the file input to be an svg document and will parse it.
    """

    def __init__(self):
        super(SvgInputMixin, self).__init__()

        self.arg_parser.add_argument(
            "--id", action="append", type=str, dest="ids", default=[],
            help="id attribute of object to manipulate")

        self.arg_parser.add_argument(
            "--selected-nodes", action="append", type=str, dest="selected_nodes", default=[],
            help="id:subpath:position of selected nodes, if any")

    def load(self, stream):
        """Load the stream as an svg xml etree and make a backup"""
        document = etree.parse(stream, parser=SVG_PARSER)
        self.original_document = copy.deepcopy(document)
        self.svg = document.getroot()
        self.svg.set_selected(*self.options.ids)
        return document


class SvgOutputMixin(object):  # pylint: disable=too-few-public-methods
    """
    Expects the output document to be an svg document and will write an etree xml.
    """

    def save(self, stream):
        """Save the svg document to the given stream"""
        document = etree.tostring(self.document)
        try:
            stream.write(document)
        except TypeError:
            stream.write(document.decode())

class SvgThroughMixin(SvgInputMixin, SvgOutputMixin):
    """
    Combine the input and output svg document handling (usually for effects.
    """

    def has_changed(self, ret): # pylint: disable=unused-argument
        """Return true if the svg document has changed"""
        original = etree.tostring(self.original_document)
        result = etree.tostring(self.document)
        return original != result
