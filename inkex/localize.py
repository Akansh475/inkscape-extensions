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
Allow extentions to translate messages.
"""

import os
import sys
import gettext

_ = gettext.gettext

def localize():
    """Turn on localisation for any platform"""
    domain = 'inkscape'
    if sys.platform.startswith('win'):
        import locale
        current_locale, _ = locale.getdefaultlocale()
        os.environ['LANG'] = current_locale
        try:
            localdir = os.environ['INKSCAPE_LOCALEDIR']
            trans = gettext.translation(domain, localdir, [current_locale], fallback=True)
        except KeyError:
            trans = gettext.translation(domain, fallback=True)
    elif sys.platform.startswith('darwin'):
        try:
            localdir = os.environ['INKSCAPE_LOCALEDIR']
            trans = gettext.translation(domain, localdir, fallback=True)
        except KeyError:
            try:
                localdir = os.environ['PACKAGE_LOCALE_DIR']
                trans = gettext.translation(domain, localdir, fallback=True)
            except KeyError:
                trans = gettext.translation(domain, fallback=True)
    else:
        try:
            localdir = os.environ['PACKAGE_LOCALE_DIR']
            trans = gettext.translation(domain, localdir, fallback=True)
        except KeyError:
            trans = gettext.translation(domain, fallback=True)
    #sys.stderr.write(str(localdir) + "\n")
    trans.install()

