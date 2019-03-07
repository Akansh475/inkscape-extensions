#!/usr/bin/env python
#
# Copyright (C) 2014  Ryan Lerch     (multiple difference)
#              2016  Maren Hachmann <marenhachmannATyahoo.com> (refactoring, extend to multibool)
#              2017  Alvin Penner   <penner@vaxxine.com> (apply to 'File Save As...')
#
# This code is based on 'inkscape-extension-multiple-difference' by Ryan Lerch
# see : https://github.com/ryanlerch/inkscape-extension-multiple-difference
# also: https://github.com/Moini/inkscape-extensions-multi-bool
# It will call up a new instance of Inkscape and process the image there,
# so that the original file is left intact.
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
This extension will pre-process a vector image by applying the operations:
'EditSelectAllInAllLayers' and 'ObjectToPath'
before calling the dialog File->Save As....
"""
from subprocess import Popen, PIPE

import os
import shutil
import inkex

class PrepareFileSave(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)

    def effect(self):
        file = self.args[-1]
        tempfile = os.path.splitext(file)[0] + "-prepare.svg"
        # tempfile is needed here only because we want to force the extension to be .svg
        # so that we can open and close it silently
        shutil.copy2(file, tempfile)
        p = Popen('inkscape --verb=EditSelectAllInAllLayers --verb=EditUnlinkClone --verb=ObjectToPath --verb=FileSaveACopy --verb=FileSave --verb=FileQuit '+tempfile, shell=True, stdout=PIPE, stderr=PIPE)
        err = p.stderr
        f = p.communicate()[0]
        err.close()


if __name__ == '__main__':
    PrepareFileSave().run()
else:
    # Skip automatic testing for this module
    raise inkex.DependencyError("This extension is untestable because of 'inkscape Popen'.")

