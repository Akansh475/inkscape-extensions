#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import platform

from distutils.version import StrictVersion

from lxml import etree

import inkex

if sys.version_info[0] == 3:  #PY3
    unicode = str  # pylint: disable=redefined-builtin,invalid-name
    basestring = str  # pylint: disable=redefined-builtin,invalid-name

try:
    import scour
    try:
        from scour.scour import scourString
    except ImportError:  # compatibility for very old Scour (<= 0.26) - deprecated!
        try:
            from scour import scourString
            scour.__version__ = scour.VER
        except:
            raise
except Exception as e:
    raise inkex.DependencyError("""Failed to import module 'scour'.
Please make sure it is installed (e.g. using 'pip install scour'
  or 'sudo apt-get install python-scour') and try again.
""")


class ScourInkscape(inkex.OutputExtension):

    def __init__(self):
        super(ScourInkscape, self).__init__()

        # Scour options
        self.arg_parser.add_argument("--tab",                      type=str,      dest="tab")
        self.arg_parser.add_argument("--simplify-colors",          type=inkex.Boolean,  dest="simple_colors")
        self.arg_parser.add_argument("--style-to-xml",             type=inkex.Boolean,  dest="style_to_xml")
        self.arg_parser.add_argument("--group-collapsing",         type=inkex.Boolean,  dest="group_collapse")
        self.arg_parser.add_argument("--create-groups",            type=inkex.Boolean,  dest="group_create")
        self.arg_parser.add_argument("--enable-id-stripping",      type=inkex.Boolean,  dest="strip_ids")
        self.arg_parser.add_argument("--shorten-ids",              type=inkex.Boolean,  dest="shorten_ids")
        self.arg_parser.add_argument("--shorten-ids-prefix",       type=str,      dest="shorten_ids_prefix", default="")
        self.arg_parser.add_argument("--embed-rasters",            type=inkex.Boolean,  dest="embed_rasters")
        self.arg_parser.add_argument("--keep-unreferenced-defs",   type=inkex.Boolean,  dest="keep_defs")
        self.arg_parser.add_argument("--keep-editor-data",         type=inkex.Boolean,  dest="keep_editor_data")
        self.arg_parser.add_argument("--remove-metadata",          type=inkex.Boolean,  dest="remove_metadata")
        self.arg_parser.add_argument("--strip-xml-prolog",         type=inkex.Boolean,  dest="strip_xml_prolog")
        self.arg_parser.add_argument("--set-precision",            type=int,      dest="digits")
        self.arg_parser.add_argument("--indent",                   type=str,      dest="indent_type")
        self.arg_parser.add_argument("--nindent",                  type=int,      dest="indent_depth")
        self.arg_parser.add_argument("--line-breaks",              type=inkex.Boolean,  dest="newlines")
        self.arg_parser.add_argument("--strip-xml-space",          type=inkex.Boolean,  dest="strip_xml_space_attribute")
        self.arg_parser.add_argument("--protect-ids-noninkscape",  type=inkex.Boolean,  dest="protect_ids_noninkscape")
        self.arg_parser.add_argument("--protect-ids-list",         type=str,      dest="protect_ids_list")
        self.arg_parser.add_argument("--protect-ids-prefix",       type=str,      dest="protect_ids_prefix")
        self.arg_parser.add_argument("--enable-viewboxing",        type=inkex.Boolean,  dest="enable_viewboxing")
        self.arg_parser.add_argument("--enable-comment-stripping", type=inkex.Boolean,  dest="strip_comments")
        self.arg_parser.add_argument("--renderer-workaround",      type=inkex.Boolean,  dest="renderer_workaround")

        # options for internal use of the extension
        self.arg_parser.add_argument("--scour-version",            type=str,      dest="scour_version")
        self.arg_parser.add_argument("--scour-version-warn-old",   type=inkex.Boolean,  dest="scour_version_warn_old")

    def save(self, stream):
        # version check if enabled in options
        if self.options.scour_version_warn_old:
            scour_version = scour.__version__
            scour_version_min = self.options.scour_version
            if StrictVersion(scour_version) < StrictVersion(scour_version_min):
                inkex.errormsg("The extension 'Optimized SVG Output' is designed for Scour " + scour_version_min + " and later "
                               "but you're using the older version Scour " + scour_version + ".")
                inkex.errormsg("This usually works just fine but not all options available in the UI might be supported "
                               "by the version of Scour installed on your system "
                               "(see https://github.com/scour-project/scour/blob/master/HISTORY.md for release notes of Scour).")
                inkex.errormsg("Note: You can permanently disable this message on the 'About' tab of the extension window.")
        del self.options.scour_version
        del self.options.scour_version_warn_old

        # do the scouring
        try:
            mystr = scourString(etree.tostring(self.document), self.options)
            try:
                stream.write(mystr)
            except Exception as e:
                mybytes = mystr.encode('utf-8') if isinstance(mystr, (str, unicode)) else mystr
                stream.write(mybytes)
        except Exception as e:
            raise
            inkex.errormsg("Error during optimization.")
            inkex.errormsg("\nDetails:\n" + str(e))
            inkex.errormsg("\nOS version: " + platform.platform())
            inkex.errormsg("Python version: " + sys.version)
            inkex.errormsg("Scour version: " + scour.__version__)

if __name__ == '__main__':
    ScourInkscape().run()
