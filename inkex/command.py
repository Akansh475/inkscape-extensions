# coding=utf-8
#
# Copyright (C) 2019 Martin Owens
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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110, USA.
#
"""
When inkscape needs to be loaded in order to ask for various compiling
options (png) running other extensions and performing options only
available via the shell API.

The preference should ALWAYS be to avoid using this API as it's very
ineffeciant to call up a new inkscape instance in order to modify
things.

The reason you SHOULD use this API instead of calling out to inkscape
yourself is because the security settings and testing functions have
been thought through and should allow you to get on with whatever
your extension does.
"""

import os
import sys
from subprocess import Popen, PIPE

from .utils import TemporaryDirectory

PY3 = sys.version_info[0] == 3

class CommandNotFound(IOError):
    """Command is not found"""
    pass

class ProgramRunError(ValueError):
    """Command returned non-zero output"""
    pass

def which(program):
    """
    Attempt different methods of trying to find if the program exists.
    """
    try:
        # Python2 and python3, but must have distutils and may not always
        # work on windows versions (depending on the version)
        from distutils.spawn import find_executable
        prog = find_executable(program)
        if prog:
            return prog
    except ImportError:
        pass

    try:
        # Python3 only version of which
        from shutil import which as warlock
        prog = warlock(program)
        if prog:
            return prog
    except ImportError:
        pass # python2

    # There may be other methods for doing a `which` command for other
    # operating systems; These should go here as they are discovered.

    raise CommandNotFound("Can not find the command: '{}'".format(program))

def write_svg(svg, *filename):
    """Writes an svg to the given filename"""
    filename = os.path.join(*filename)
    if os.path.isfile(filename):
        return filename
    with open(filename, 'wb') as fhl:
        if hasattr(svg, 'write'):
            # XML document
            svg.write(fhl)
        elif isinstance(svg, bytes):
            fhl.write(svg)
        else:
            raise ValueError("Not sure what type of SVG data this is.")
    return filename


def to_arg(arg, oldie=False):
    """Convert a python argument to a command line argument"""
    if isinstance(arg, (tuple, list)):
        (arg, val) = arg
        arg = '-' + arg
        if len(arg) > 2 and not oldie:
            arg = '-' + arg
        if val is True:
            return arg
        if val is False:
            return None
        return '{}={}'.format(arg, str(val))
    return str(arg)

def to_args(prog, *positionals, **arguments):
    """
    Convert positional arguments and key word arguments
    into a list of strings which Popen will understand.

    Values can be:

    args = *[
        'strait_up_string',
        '--or_manual_kwarg=1',
        ('ordered list', 'version of kwargs (as below)'),
        ...
    ]
    kwargs = **{
        'name': 'val',          # --name="val"'
        'name': ['foo', 'bar'], # --name=foo --name=bar
        'name': True,           # --name
        'n': 'v',               # -n=v
        'n': True,              # -n
    }

    All args appear after the kwargs, so if you need args before,
    use the ordered list tuple and don't use kwargs.
    """
    args = [prog]
    oldie = arguments.pop('oldie', False)
    for arg, value in arguments.items():
        arg = arg.replace('_', '-').strip()

        if isinstance(value, tuple):
            value = list(value)
        elif not isinstance(value, list):
            value = [value]

        for val in value:
            args.append(to_arg((arg, val), oldie))

    args += [to_arg(pos, oldie) for pos in positionals]
    # Filter out empty non-arguments
    return [arg for arg in args if arg is not None]

def _call(program, *args, **kwargs):
    stdin = kwargs.pop('stdin', None)
    if PY3 and isinstance(stdin, str):
        stdin = stdin.encode('utf-8')
    inpipe = PIPE if stdin else None

    process = Popen(
        to_args(which(program), *args, **kwargs),
        shell=False, # Never have shell=True
        stdin=inpipe, # StdIn not used (yet)
        stdout=PIPE, # Grab any output (return it)
        stderr=PIPE, # Take all errors, just incase
    )
    (stdout, stderr) = process.communicate(input=stdin)
    if process.returncode == 0:
        return stdout
    raise ProgramRunError("Return Code: {}: {}\n{}".format(process.returncode, stderr, stdout))

def call(program, *args, **kwargs):
    """
    Generic caller to open any program and return it's stdout.

    stdout = call('executable', arg1, arg2, dash_dash_arg='foo', d=True, ...)

    Will raise ProgramRunError() if return code is not 0.
    """
    return _call(program, *args, **kwargs)

def inkscape(svg_file, *args, **kwargs):
    """
    Call inkscape with the given svg_file and the given arguments
    """
    return call('inkscape', svg_file, without_gui=True, *args, **kwargs)

def inkscape_command(svg, *verbs):
    """
    Executes a list of verbs on the given svg (svg as a string, not a filename).

    inkscape_command('<svg...>', 'UnlockAllInAllLayers', 'ObjectToPath')

    Returns the resulting svg string (not the filename!)
    """
    with TemporaryDirectory(prefix='inkscape-command') as dirname:
        svg_file = write_svg(svg, dirname, 'input.svg')
        inkscape(svg_file, verb=list(verbs) + ['FileSave', 'FileQuit'])
        with open(svg_file, 'rb') as fhl:
            return fhl.read()


def take_snapshot(svg, dirname, name='snapshot', ext='png', dpi=96, **kwargs):
    """
    Takes a snapshot of the given svg file.

    Resulting filename is yielded back, after generator finishes, the
    file is deleted so you must deal with the file inside the for loop.
    """
    svg_file = write_svg(svg, dirname, name + '.svg')
    ext_file = os.path.join(dirname, name + '.' + str(ext).lower())
    kwargs['export_' + ext] = ext_file
    inkscape(svg_file, export_dpi=dpi, **kwargs)
    return ext_file
