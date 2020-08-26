#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Martin Owens <doctormo@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>
#
"""
Bootstrap the inkscape extensions manager setting up the virtualenv
and adding the extensions package.
"""

import os

import inkex
from inkex.utils import get_user_directory
from inkex.base import InkscapeExtension
from inkex.command import CommandNotFound, ProgramRunError, call

try:
    from manage_extensions import run as run_existing
except ImportError:
    run_existing = None

TARGET_DIR = get_user_directory()

class Bootstrap(InkscapeExtension):
    multi_inx = True

    def add_arguments(self, pars):
        pars.add_argument('--tab')
        pars.add_argument('--version', default='inkscape-extensions-manager')

    def load_raw(self):
        pass

    def save_raw(self, ret):
        self.msg("Installation Successful!")

    def effect(self):
        try:
            call('virtualenv', TARGET_DIR, p='python3')
        except CommandNotFound:
            raise inkex.AbortExtension(
                "You must have the python-virtualenv package installed. This should have"
                " been included with Inkscape, but in some special cases it might not"
                " be. Please install this software externally and try again.")
        except ProgramRunError as err:
            raise inkex.AbortExtension(
                "There has been a problem creating the python environment:\n" + str(err))

        try:
            call(os.path.join(TARGET_DIR, 'bin', 'pip'), 'install', self.options.version)
        except CommandNotFound:
            raise inkex.AbortExtension("Can't find pip program after environment initialisation!")
        except ProgramRunError as err:
            raise inkex.AbortExtension("Error installing extension manager package:\n" + str(err))

if __name__ == '__main__':
    if run_existing is not None:
        # If the extension manager is already installed
        # Run it instead of the bootstrap process.
        run_existing()
    else:
        Bootstrap().run()
