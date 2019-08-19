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
Allow extensions to translate messages.
"""

import gettext
import os
import sys

_ = gettext.gettext

# The default gettext domain is 'inkscape' this is because previously
# we used the central translation dictionary for the translations
# and now we want to support extensions that have their own.
GETTEXT_DOMAIN = os.environ.get('INKEX_GETTEXT_DOMAIN', 'inkscape')

# The package locale dir is primary, inkscape is secondary and finally
# is None, which should default to the system settings.
LOCALEDIR = os.environ.get('PACKAGE_LOCALE_DIR', \
    os.environ.get('INKSCAPE_LOCALEDIR', None))

def localize(domain=GETTEXT_DOMAIN, localdir=LOCALEDIR):
    """Turn on localisation for any platform"""
    languages = None
    if sys.platform.startswith('win'):
        import locale
        current_locale, _ = locale.getdefaultlocale()
        os.environ['LANG'] = current_locale
        languages = [current_locale]

    # sys.stderr.write(str(localdir) + "\n")
    trans = gettext.translation(domain, localdir, languages, fallback=True)
    trans.install()
