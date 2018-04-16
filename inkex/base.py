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
The utimate base functionality for every inkscape extension.
"""

import sys
import copy

from argparse import ArgumentParser

from .utils import filename_arg
from .svg import etree, SVG_PARSER

class InkscapeExtension(object):
    """
    The base class extension, provides argument parsing and basic
    variable handling features.
    """
    def __init__(self):
        self.options = None
        self.document = None
        self.arg_parser = ArgumentParser(description=self.__doc__)

        self.arg_parser.add_argument(
            "input_file", nargs="?", metavar="INPUT_FILE", type=filename_arg,
            help="Filename of the input file (default is stdin)", default=sys.stdin)

        self.arg_parser.add_argument(
            "--output", type=str, default=sys.stdout,
            help="Optional output filename for saving the result (default is stdout).")

    def run(self, args=sys.argv[1:], output=True, input_=True):
        """Main entrypoint for any Inkscape Extension"""
        self.options = self.arg_parser.parse_args(args)

        if input_:
            if isinstance(self.options.input_file, str):
                with open(self.options.input_file, 'rb') as stream:
                    self.document = self.load(stream)
            else:
                self.document = self.load(self.options.input_file)

        self.effect()

        if output and self.has_changed():
            if isinstance(self.options.output, str):
                with open(self.options.output, 'wb') as stream:
                    self.save(stream)
            else:
                self.save(self.options.output)

    @staticmethod
    def has_changed():
        """Returns if the effect has changed the document or not (always True)"""
        return True

    def load(self, stream):
        """Takes the input stream and creates a document for parsing"""
        raise NotImplementedError("No input handle for {}".format(self.name))

    def save(self, stream):
        """Save the given document to the output file"""
        raise NotImplementedError("No output handle for {}".format(self.name))

    def effect(self):
        """Apply some effects on the document or local context"""
        raise NotImplementedError("No effect handle for {}".format(self.name))

    @property
    def name(self):
        """Return a fixed name for this extension"""
        return type(self).__name__


class SvgInputMixin(object): # pylint: disable=too-few-public-methods
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


class SvgOutputMixin(object): # pylint: disable=too-few-public-methods
    """
    Expects the output document to be an svg document and will write an etree xml.
    """
    def save(self, stream):
        """Save the svg document to the given stream"""
        self.document.write(stream)


class SvgThroughMixin(SvgInputMixin, SvgOutputMixin):
    """
    Combine the input and output svg document handling (usually for effects.
    """
    def has_changed(self):
        """Return true if the svg document has changed"""
        original = etree.tostring(self.original_document)
        result = etree.tostring(self.document)
        return original != result

