#
# Copyright (C) 2008 Stephen Silver
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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA
#
"""
Module for running SVG-generating commands in Inkscape extensions
"""
import os
import sys
import tempfile


def run(command_format, prog_name):
    """
    Run a command that generates an SVG (or PDF) file from an input file.

    On success, outputs the contents of the resulting file to stdout, and exits
     with a return code of 0.

    On failure, outputs an error to stderr, and exits with a return code of 1.
    """
    svgfile = tempfile.mktemp(".svg")
    command = command_format % svgfile
    msg = None
    # ps2pdf may attempt to write to the current directory, which may not
    # be writeable, so we switch to the temp directory first.
    try:
        os.chdir(tempfile.gettempdir())
    except IOError:
        pass
    # In order to get a return code from the process, we use subprocess.Popen
    # if it's available (Python 2.4 onwards) and otherwise use popen2.Popen3
    # (Unix only).  As the Inkscape package for Windows includes Python 2.5,
    # this should cover all supported platforms.
    try:
        try:
            from subprocess import Popen, PIPE
            proc = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
            return_code = proc.wait()
            out = proc.stdout.read()
            err = proc.stderr.read()
        except ImportError:
            try:
                from popen2 import Popen3
                proc3 = Popen3(command, True)
                proc3.wait()
                return_code = proc3.poll()
                out = proc3.fromchild.read()
                err = proc3.childerr.read()
            except ImportError:
                # shouldn't happen...
                msg = "Neither subprocess.Popen nor popen2.Popen3 is available"
        if msg is None:
            if return_code:
                msg = "%s failed:\n%s\n%s\n" % (prog_name, out, err)
            elif err:
                sys.stderr.write("%s executed but logged the following error:\n%s\n%s\n" % (prog_name, out, err))
    except Exception as inst:
        msg = "Error attempting to run %s: %s" % (prog_name, str(inst))

    # If successful, copy the output file to stdout.
    if msg is None:
        if os.name == 'nt':  # make stdout work in binary on Windows
            import msvcrt
            msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
        try:
            with open(svgfile, "rb") as fhl:
                sys.stdout.write(fhl.read())
        except IOError, inst:
            msg = "Error reading temporary file: %s" % str(inst)

    try:
        # Clean up.
        os.remove(svgfile)
    except (IOError, OSError):
        pass

    # Output error message (if any) and exit.
    return msg


# vim: expandtab shiftwidth=4 tabstop=8 softtabstop=4 fileencoding=utf-8 textwidth=99
